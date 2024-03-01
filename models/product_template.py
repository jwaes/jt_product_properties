import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    tmpl_property_kv_ids = fields.One2many('jt.property.kv', 'product_template_id', string='Template Property fields')
    tmpl_all_kvs = fields.One2many('jt.property.kv', compute='_compute_all_kvs', recursive=True, string='All template KVS' )

    has_active_attributes = fields.Boolean('has_active_attributes', compute='_compute_has_active_attributes')
    
    @api.depends('valid_product_template_attribute_line_ids')
    def _compute_has_active_attributes(self):
        for record in self:
            record.has_active_attributes = record.valid_product_template_attribute_line_ids._without_no_variant_attributes().product_template_value_ids._only_active()

    @api.depends('tmpl_property_kv_ids','categ_id','categ_id.all_kvs')
    def _compute_all_kvs(self):
        for tmpl in self:
            kvs = tmpl.tmpl_property_kv_ids

            all_parental_kvs = self.env['jt.property.kv']
            _logger.debug("getting properties for product.template %s", tmpl.name)

            if tmpl.categ_id:
                all_parental_kvs = tmpl.categ_id.all_kvs
            _logger.debug("all_parental_kvs length for %s is %s", tmpl.name, len(all_parental_kvs))

            for kv in tmpl.tmpl_property_kv_ids:
                #looking for values in parental map to remove
                if kv.key_id.behavior == 'replace':
                    all_parental_kvs = all_parental_kvs.filtered(lambda kvi: kvi.code != kv.code)
            _logger.debug("after filtering, all_parental_kvs length for %s is %s", tmpl.name, len(all_parental_kvs))

            #now merging new values
            tmpl.tmpl_all_kvs = all_parental_kvs | tmpl.tmpl_property_kv_ids
            _logger.debug("final all kvs count in %s : %s", tmpl.name, len(tmpl.tmpl_all_kvs))
 
            # _logger.info("┌──[TPL] %s ", tmpl.name)
            # for kvl in tmpl.tmpl_all_kvs:
            #     _logger.info("├─ %s : %s", kvl.code, kvl.text)   