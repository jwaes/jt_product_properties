# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class PropertyKV(models.Model):
    _name = 'jt.property.kv'
    _description = 'Property key/value pair'
    _inherit = 'jt.property.mixin'

    ref_id = fields.Many2one('jt.property.mixin', string='Reference', required=True)

    # key_id = fields.Many2one('jt.property.key', string='Key', required=True)
    
    #one of these values is valid, depending on the key.property_type
    value_id = fields.Many2one('jt.property.value', string='Value')
    text = fields.Char('text')
    html = fields.Text('html')
    

    # category_id = fields.Many2one('product.category', string='Category')
    # product_id = fields.Many2one('product.product', string='Product Variant')
    # product_tmpl_id = fields.Many2one('product.template', string='Product')    
    