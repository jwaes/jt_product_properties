import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"

    property_kv_ids = fields.One2many('jt.property.kv', 'product_id', string='Property fields')
    all_kvs = fields.One2many('jt.property.kv', compute='_compute_all_kvs', order='key_id')

    @api.depends('property_kv_ids')
    def _compute_all_kvs(self):
        kvs = self.property_kv_ids

        all_parental_kvs = self.env['jt.property.kv']

        # if self.categ_id:
        #     all_parental_kvs = self.categ_id.all_kvs
        # _logger.debug("all_parental_kvs length for %s is %s", self.name, len(all_parental_kvs))
        _logger.debug("getting properties for product.product %s", self.name)
        all_parental_kvs = self.product_tmpl_id.tmpl_all_kvs

        for kv in self.property_kv_ids:
            #looking for values in parental map to remove
            if kv.key_id.behavior == 'replace':
                all_parental_kvs = all_parental_kvs.filtered(lambda kvi: kvi.code != kv.code)
        _logger.debug("after filtering, all_parental_kvs length for %s is %s", self.name, len(all_parental_kvs))

        #now merging new values
        self.all_kvs = all_parental_kvs | self.property_kv_ids
        _logger.debug("final all kvs count in %s : %s", self.name, len(self.all_kvs))