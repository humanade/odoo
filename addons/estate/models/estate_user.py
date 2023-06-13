from odoo import fields, models

class UserProperty(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "salesperson_id", domain="['state', '!=', 'S'], ['state', '!=', 'C']", string="Propriétés")
