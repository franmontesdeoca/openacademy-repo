# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import models, fields, api, exceptions
from odoo.exceptions import ValidationError

class History(models.Model):
    _name = 'medical.history'
    _order = 'create_date desc'
    INVENTORY_STATE_SELECTION = [
        ('female', 'Female'),
        ('male', 'Male'),
        ('others', 'Others')]
    INVENTORY_TYPE_SELECTION = [
        ('new_patient', 'New Patient'),
        ('frequent', 'Frequent'),
        ('recurrent', 'Recurrent')]
    name = fields.Many2one('res.partner', string="patient" , required=True)
    description = fields.Html(string="Description")
    identification_card = fields.Char(string="C.I")
    responsibe_id=fields.Many2one('res.users',string="Doctor",index=True, ondelete='set null', required=True)
    details_ids =fields.One2many('medical.details','task_id', string="History")
    birth_date = fields.Date(string="Birth Date")
    home = fields.Text(string="Home")
    mail = fields.Char(string="Mail")
    phone = fields.Char(string="Phone")
    insurance = fields.Char(string="Insurance")
    other_data = fields.Text(string="Other Data")
    color = fields.Float(digits=(6, 0), string="Definido por Colores") #para vista kanban
    sex = fields.Selection(selection=INVENTORY_STATE_SELECTION,string='Sex', default='')
    type_id = fields.Selection(selection=INVENTORY_TYPE_SELECTION,string='Type', default='')
    warehouse_id = fields.Many2one('stock.warehouse',string="Medical Center",index=True, ondelete='set null')
    #para vista grefico
    attendees_count = fields.Integer(
        string="Visitas por Pacientes", compute='_get_attendees_count', store=True) 
    #para vista grefico
    @api.depends('details_ids')
    def _get_attendees_count(self):
        for r in self:
            r.attendees_count = len(r.details_ids)
    
    #Valida que no se repita un registro
    @api.constrains('instructor_id', 'attendee_ids')
    @api.constrains('name', 'responsibe_id')
    def _check_instructor_not_in_attendees(self):
        for r in self:
            if r.name and r.name in r.home:
                raise exceptions.ValidationError("A session's patient can't be an doctor")
    
    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "The title of the course should not be the description"),

        ('name_unique',
         'UNIQUE(name)',
         "The patient's name must be Unique"),
    ]
    # api para copiar o ducplicar un registro
    @api.multi
    def copy(self, default=None):
        default = dict(default or {})
        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(History, self).copy(default)

class details(models.Model):
    _name = 'medical.details'
    _order = 'create_date desc'
    INVENTORY_STATES_SELECTION = [
        ('active', 'Active'),
        ('inactive', 'Inactive')]
    name = fields.Char(required=True,string="Data")
    date = fields.Date(string="Date",default=fields.Date.today)
    next_appointment = fields.Date(string="Next Appointment")
    pressure = fields.Float(digits=(6, 0),string="Pressure")
    temperature = fields.Float(digits=(6, 0),string="Temperature")
    prod_ids =fields.One2many('medical.recipe','recipe_id', string="Product Recipe")
    #duration = fields.Date.from_string(item.start_date) - fields.Date.from_string(fields.Date.context_today(self))
    instructor_id = fields.Many2one('res.partner', string="Responsible")
    task_id = fields.Many2one('medical.history',
        ondelete='cascade', string="Patient", required=True)
    state = fields.Selection(selection=INVENTORY_STATES_SELECTION,string='State', default='active')
    recipe_ids =fields.Many2many('product.template',string='Recipe')
    details = fields.Html(string="Prescription")
    height=fields.Char(string="Height")
    cost = fields.Float(digits=(6, 2), string="appointment cost")
    diagnostic = fields.Html(string="Diagnostic")
    

    #@api.onchange('pressure', 'temperature')
    #def _onchange_price(self):
        
    #    self.cost = self.pressure * self.temperature
        
        #return {
        #    'warning': {
         #       'title': "Something bad happened",
        #        'message': "It was very bad indeed",
        #    }
        #}
class prod(models.Model):
    _name = 'medical.recipe'

    products_id=fields.Many2one('product.template',string="Product",index=True, ondelete='set null',required=True)
    quantity = fields.Float(digits=(3, 0), default='1', help="Quantity in Products")
    recipe_id = fields.Many2one('medical.details')
