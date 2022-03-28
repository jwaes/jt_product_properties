# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class PropertyKV(models.Model):
    _name = 'jt.property.kv'
    _description = 'Property key/value pair'

    key_id = fields.Many2one('jt.property.key', string='Key', required=True)

    # 'name_template' : fields.related('product_id','name_template', type='char', string='Name Template',store=True),
    property_type = fields.Selection(related='key_id.property_type', tracking=True)

    # one of these values is valid, depending on the key.property_type
    value_id = fields.Many2one('jt.property.value', string='Value', domain="[('key_id', '=', key_id)]")
    text = fields.Char('text')
    html = fields.Text('html')

    category_id = fields.Many2one('product.category', string='Category')
    product_id = fields.Many2one('product.product', string='Product Variant')
    product_template_id = fields.Many2one('product.template', string='Product')

    reference_name = fields.Char('Reference name', default='[]')

    # @api.depends('category_id','product_id','product_template_id')
    # @api.onchange('category_id','product_id','product_template_id')    
    # def _compute_reference_name(self):
    #     _logger.debug("product_id is %s", self.product_id)
    #     _logger.debug("template_id is %s", self.product_template_id)
    #     _logger.debug("category_id is %s", self.category_id)        
    #     self.reference_name = '[]'
    #     if self.category_id:
    #         _logger.debug("found categ")
    #         self.reference_name = '[CAT]'
    #     elif self.product_template_id:
    #         _logger.debug("found templ")
    #         self.reference_name = '[TMPL] {}'.format(self.product_template_id.name)        
    #     elif self.product_id:
    #         _logger.debug("found product")
    #         self.reference_name = '[PROD] {}'.format(self.product_id.name)

    @api.onchange('category_id')
    @api.depends('category_id')
    def onchange_cat_id(self):
        if self.reference_name != "[]":
            self.reference_name = "CAT"

    @api.onchange('product_id')
    @api.depends('product_id')
    def onchange_prod_id(self):
        if self.reference_name != "[]":
            self.reference_name = "PROD"            

    
    @api.onchange('property_type')
    def onchange_property_type(self):
        if self.property_type == 'select':
            self.text = None
            self.html = None
        elif self.property_type == 'free_text':
            self.html = None
            self.value_id = None
        elif self.property_type == 'html':
            self.text = None
            self.value_id = None

    def write(self, vals):
        super().write(vals)
        self.onchange_property_type(self)
        return True        
