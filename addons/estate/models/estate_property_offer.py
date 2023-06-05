from odoo import models, fields, api, exceptions
from datetime import date, timedelta

class EstatePropertyOffer(models.Model):
    def get_my_list():
        return [('R', 'Offre refusée'), 
                ('A', 'Offre acceptée')]
    
    _name = "estate.property.offer"
    _description = "An offer on a property"
    _order = "price desc"

    price = fields.Float('Montant', required=True)
    status = fields.Selection(selection=get_my_list(), string='Statut')
    partner_id = fields.Many2one('res.partner', string='Partenaire')
    property_id = fields.Many2one('estate.property', string='Propriété')
    validity_days = fields.Integer(string='Validité', default=7)
    deadline_date = fields.Date(string='Date de fin de validité', compute='_compute_deadline', inverse='_inverse_deadline')
    
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price >= 0)', 'Le montant de l''offre doit être positif.')
    ]

    @api.depends('validity_days')
    def _compute_deadline(self):
        for record in self:
            record.deadline_date = date.today() + timedelta(days=record.validity_days)
    
    def _inverse_deadline(self):
        for record in self:
            record.validity_days = (record.deadline_date - date.today()).days

    def accept_offer(self):
        for record in self:
            for offer in record.property_id.offer_ids:
                if offer.status == 'A':
                    raise exceptions.UserError('Une offre a déja été acceptée')
            
            record.status = 'A'
            record.property_id.status = 'A'
            record.property_id.buyer_id = self.partner_id
            record.property_id.selling_price = self.price
            return True

    def refuse_offer(self):
        for record in self:
            if record.status == 'A':
                record.property_id.status = 'R'
                record.property_id.buyer_id = None
                record.property_id.selling_price = 0

            record.status = 'R'
            return True
    
    