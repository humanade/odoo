from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of the real estate good"

    name = fields.Char('Libellé', required=True)
