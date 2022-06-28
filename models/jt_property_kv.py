# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class PropertyKV(models.Model):
    _name = 'jt.property.kv'
    _description = 'Property key/value pair'

    key_id = fields.Many2one('jt.property.key', string='Key', required=True)

    # 'name_template' : fields.related('product_id','name_template', type='char', string='Name Template',store=True),
    property_type = fields.Selection(related='key_id.property_type')
    code = fields.Char(related='key_id.code')

    # one of these values is valid, depending on the key.property_type
    value_id = fields.Many2one(
        'jt.property.value', string='Value', domain="[('key_id', '=', key_id)]")
    text = fields.Char('text', translate=True)
    html = fields.Text('html', translate=True)

    category_id = fields.Many2one('product.category', string='Category')
    product_id = fields.Many2one('product.product', string='Product Variant')
    product_template_id = fields.Many2one('product.template', string='Product')

    ref_name = fields.Char('Reference', compute='_compute_reference_name')

    url = fields.Char(compute='_compute_url', compute_sudo=True, string='url')

    possible_product_template_attribute_value_ids = fields.Many2many('product.template.attribute.value',
        compute='_compute_possible_product_template_attribute_value_ids')

    product_template_attribute_value_ids = fields.Many2many(
        'product.template.attribute.value', string="Apply on Variants", ondelete='restrict',
        domain="[('id', 'in', possible_product_template_attribute_value_ids)]",
        help="BOM Product Variants needed to apply this line.")

    @api.depends(
        'product_template_id.attribute_line_ids.value_ids',
        'product_template_id.attribute_line_ids.attribute_id.create_variant',
        'product_template_id.attribute_line_ids.product_template_value_ids.ptav_active',
    )
    def _compute_possible_product_template_attribute_value_ids(self):
        for record in self:
            record.possible_product_template_attribute_value_ids = record.product_template_id.valid_product_template_attribute_line_ids._without_no_variant_attributes().product_template_value_ids._only_active()

    @api.depends('value_id')
    def _compute_url(self):
        for rec in self:
            if rec.value_id.page_id:
                rec.url = rec.value_id.page_id.url
            else:
                rec.url = None

    def _compute_reference_name(self):
        for rec in self:
            _logger.debug("code is %s", rec.code)
            _logger.debug("product_id is %s", rec.product_id)
            _logger.debug("template_id is %s", rec.product_template_id)
            _logger.debug("category_id is %s", rec.category_id)
            rec.ref_name = '[]'
            if rec.category_id:
                _logger.debug("found categ")
                rec.ref_name = '[CAT] {}'.format(rec.category_id.name)
            elif rec.product_template_id:
                _logger.debug("found templ")
                rec.ref_name = '[TMPL] {}'.format(rec.product_template_id.name)
            elif rec.product_id:
                _logger.debug("found product")
                rec.ref_name = '[PROD] {}'.format(rec.product_id.name)

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
