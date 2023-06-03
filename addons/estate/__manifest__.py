# -*- coding: utf-8 -*-

{
    'name': 'Estate',
    'version': '0.1',
    'category': 'Sales/Estate',
    'sequence': 15,
    'summary': 'Track real estate offers and sales',
    'description': "",
    'depends': [
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}
