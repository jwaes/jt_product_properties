import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"

    property_kv_ids = fields.One2many('jt.property.kv', 'product_id', string='Variant Property fields')
    all_kvs = fields.One2many('jt.property.kv', compute='_compute_all_kvs')

    @api.depends('property_kv_ids')
    def _compute_all_kvs(self):
        for record in self:

            kvs = record.property_kv_ids

            all_parental_kvs = self.env['jt.property.kv']

            _logger.debug("getting properties for product.product %s", record.name)
            all_parental_kvs = record.product_tmpl_id.tmpl_all_kvs

            for parent_kv in all_parental_kvs:
                if parent_kv.product_template_attribute_value_ids:                    
                    for ptav in parent_kv.product_template_attribute_value_ids:
                        if ptav not in record.product_template_variant_value_ids:
                            #filtering out values set on the template but not applicable for this variant
                            _logger.debug("ptav %s was not in the list of applicables, removing", ptav)
                            all_parental_kvs = all_parental_kvs.filtered(lambda kvi: ptav not in kvi.product_template_attribute_value_ids)

            for kv in record.property_kv_ids:
                #looking for values in parental map to remove
                if kv.key_id.behavior == 'replace':
                    all_parental_kvs = all_parental_kvs.filtered(lambda kvi: kvi.code != kv.code)
            _logger.debug("after filtering, all_parental_kvs length for %s is %s", record.name, len(all_parental_kvs))

            #now merging new values
            record.all_kvs = all_parental_kvs | record.property_kv_ids
            _logger.debug("final all kvs count in %s : %s", record.name, len(record.all_kvs))