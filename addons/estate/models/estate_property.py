from odoo import models, fields, api, exceptions, tools
from datetime import date
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    def get_my_list():
        return [('N', 'New'),
                ('R', 'Offer Received'),
                ('A', 'Offer Accepted'),
                ('S', 'Sold'),
                ('C', 'Canceled')]
    def get_orientations():
        return [('N', 'North'), ('W', 'West'), ('S', 'South'), ('E', 'East')]

    _name = "estate.property"
    _description = "Description of the real estate good"
    _order = "id desc"

    active = fields.Boolean('Actif', default=True, invisible="1")
    state = fields.Selection(selection=get_my_list(), required=True, default='N')
    name = fields.Char('Libellé', required=True)
    description = fields.Char('Description', required=True)
    postal_code = fields.Char('Code Postal', required=True)
    availibility_date = fields.Date('Date de disponibilité', default=date.today() + relativedelta(months=+3))
    expected_price = fields.Float('Prix affiché')
    selling_price = fields.Float('Prix de vente accepté', readonly=True)
    best_offer = fields.Float(compute='_compute_best_offer', string="Meilleure offre", readonly=True)
    number_of_bedrooms = fields.Integer('Nombre de chambre', required=True, default=2)
    garage = fields.Boolean('Garage', default=False)
    garden = fields.Boolean('Jardin', default=False)
    garden_area = fields.Integer('Surface extérieure')
    orientation = fields.Selection(selection=get_orientations())
    living_area = fields.Integer('Surface intérieure', required=True)
    total_area = fields.Integer(compute='_compute_total_area', string="Surface totale")
    property_type_id = fields.Many2one("estate.property.type", string="Type de propriété")
    salesperson_id = fields.Many2one("res.users", string="Commercial", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Acheteur", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags", copy=False)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offres")

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >= 0)', 'Le prix affiché doit être positif.')
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for record in self:
            max_offer = 0
            for offer in record.offer_ids:
                if max_offer <= offer.price:
                    max_offer = offer.price
            record.best_offer = max_offer

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden == True:
                record.garden_area = 200
                record.orientation = 'N'

    @api.ondelete(at_uninstall=False)
    def _do_not_delete_if_state_is_not_appropriate(self):
        for record in self:
            if record.state == 'S' or record.state == 'A':
                raise exceptions.UserError("On ne peut supprimer une propriété avec une offre acceptée ou vendue")

    def set_property_to_new(self):
        for record in self:
            record.state = 'N'
            return True

    def set_property_to_sold(self):
        for record in self:
            if record.state == 'C':
                return exceptions.UserError('Cannot sell a canceled property')
            record.state = 'S'
            return True

    def set_property_to_canceled(self):
        for record in self:
            record.state = 'C'
            return True
        
    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if not tools.float_utils.float_is_zero(record.selling_price, precision_rounding=None, precision_digits=2):
                if tools.float_utils.float_compare(record.selling_price, record.expected_price*0.90, precision_rounding=None, precision_digits=2) < 0:
                    raise exceptions.ValidationError("Le montant est inférieur à 90% du montant voulu")
