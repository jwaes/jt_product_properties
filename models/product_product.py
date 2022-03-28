import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"

    property_kv_ids = fields.One2many('jt.property.kv', 'product_id', string='Property fields')
    all_kvs = fields.One2many('jt.property.kv', compute='_compute_all_kvs', order='key_id')

    @api.depends('property_kv_ids')
    def _compute_all_kvs(self):
        _logger.debug("Getting all kvs")
        _logger.debug("kvs count in %s : %s",self.name, len(self.property_kv_ids))
        kvs = self.property_kv_ids
        if self.categ_id:
            _logger.debug("adding category kvs")
            kvs = kvs | self.categ_id.all_kvs
        # add template kvs ?
        _logger.debug("kvs count in %s : %s", self.name, len(self.property_kv_ids))
        self.all_kvs = kvs