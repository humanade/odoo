from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    def get_my_list():
        return [('N', 'New'), 
                ('R', 'Offer Received'), 
                ('A', 'Offer Accepted'), 
                ('S', 'Sold'), 
                ('C', 'Canceled')]

    _name = "estate.property"
    _description = "Description of the real estate good"

    active = fields.Boolean('Actif', default=True, invisible="1")
    status = fields.Selection(selection=get_my_list(), required=True, default='N')
    name = fields.Char('Libellé', required=True)
    description = fields.Char('Description', required=True)
    postal_code = fields.Char('Code Postal', required=True)
    availibility_date = fields.Date('Date de disponibilité', default=date.today() + relativedelta(months=+3))
    expected_price = fields.Float('Prix minimum')
    selling_price = fields.Float('Prix de vente affiché')
    best_offer = fields.Float(compute='_compute_best_offer', string="Meilleure offre")
    number_of_bedrooms = fields.Integer('Nombre de chambre', required=True, default=2)
    garage = fields.Boolean('Garage', default=False)
    garden = fields.Boolean('Jardin', default=False)
    garden_area = fields.Integer('Surface extérieure', required=True)
    living_area = fields.Integer('Surface intérieure', required=True)
    total_area = fields.Integer(compute='_compute_total_area', string="Surface totale")
    property_type_id = fields.Many2one("estate.property.type", string="Type de propriété")
    salesperson_id = fields.Many2one("res.users", string="Commercial", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Acheteur", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags", copy=False)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offres")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        self.total_area = self.living_area + self.garden_area
    
    @api.depends('offer_ids')
    def _compute_best_offer(self):
        max_offer = 0
        for offer in self.offer_ids:
            if max_offer <= offer.price:
                max_offer = offer.price
        self.best_offer = max_offer
