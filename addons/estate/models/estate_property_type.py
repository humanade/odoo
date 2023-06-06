from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of the real estate good"
    _order = "name"

    name = fields.Char('Libellé', required=True)
    line_ids = fields.One2many("estate.property", "property_type_id", string="Propriétés")

    _sql_constraints = [
        ('check_type_name', 'UNIQUE (name)', 'Il existe déjà un type avec ce libellé')
    ]