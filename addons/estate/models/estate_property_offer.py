from odoo import models, fields, api
from datetime import date, timedelta

class EstatePropertyType(models.Model):
    def get_my_list():
        return [('R', 'Offre refusée'), 
                ('A', 'Offre acceptée')]
    
    _name = "estate.property.offer"
    _description = "An offer on a property"

    price = fields.Float('Prix', required=True)
    status = fields.Selection(selection=get_my_list(), string="Statut")
    partner_id = fields.Many2one("res.partner", string="Partenaire", required=True)
    property_id = fields.Many2one("estate.property", string="Propriété", required=True)
    validity_days = fields.Integer(string='Validité (jours)', default=7)
    deadline_date = fields.Date(compute='_compute_deadline', inverse='_inverse_deadline', string='Date de fin de validité')

    @api.depends('validity_days')
    def _compute_deadline(self):
        self.deadline_date = date.today() + timedelta(days=self.validity_days)
        print('Validity date: ' + str(self.deadline_date))

    def _inverse_deadline(self):
        self.validity_days = (self.deadline_date - date.today()).days
        print('Days: ' + self.validity_days)
    