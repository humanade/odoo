from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag for properties"
    _order = "name"

    name = fields.Char('Libellé', required=True)
    color = fields.Integer('Couleur')

    _sql_constraints = [
        ('check_tag_name', 'UNIQUE (name)', 'Il existe déjà un tag avec ce libellé')
    ]
