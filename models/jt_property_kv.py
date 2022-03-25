# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class PropertyKV(models.Model):
    _name = 'jt.property.kv'
    _description = 'Property key/value pair'

    

    category_id = fields.Many2one('product.category', string='Category')
    product_id = fields.Many2one('product.product', string='Product Variant')
    product_tmpl_id = fields.Many2one('product.template', string='Product')    
    