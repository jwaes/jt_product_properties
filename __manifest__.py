# -*- coding: utf-8 -*-
{
    'name': "jt_product_properties",

    'summary': "Product properties key/value pairs",

    'description': "",

    'author': "jaco tech",
    'website': "https://jaco.tech",
    "license": "AGPL-3",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customizations',
    'version': '2.0',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','website'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/jt_property_key.xml',
        'views/jt_property_settings.xml',
        'views/product_category.xml',
        'views/product_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
