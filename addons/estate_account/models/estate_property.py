from odoo import models, fields, Command

class EstateProperty(models.Model):
    _inherit = "estate.property"

    account_move_id = fields.Many2one("account.move", string="Facture correspondante")

    def set_property_to_sold(self):
        for record in self:
            dict = {
                'move_type': 'out_invoice',
                'partner_id': record.buyer_id.id,
                'line_ids': [
                    Command.create({
                        'name': "Vente de la propriété" + record.name,
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': "Selling fees",
                        'quantity': 1,
                        'price_unit': 100,
                    })
                ],
            }
            record.account_move_id = self.env["account.move"].create(dict)
        return super().set_property_to_sold()
