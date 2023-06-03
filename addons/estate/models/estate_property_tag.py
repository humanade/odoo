from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.tag"
    _description = "Tag for properties"

    name = fields.Char('Libellé', required=True)
