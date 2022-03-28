import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class ProductCategory(models.Model):
    _inherit = 'product.category'

    property_kv_ids = fields.One2many('jt.property.kv', 'category_id', string='Property fields')
    all_kvs = fields.One2many('jt.property.kv', compute='_compute_all_kvs', order='key_id')

    @api.depends('property_kv_ids')
    def _compute_all_kvs(self):
        _logger.debug("Getting all kvs")
        _logger.debug("kvs count in %s : %s",self.name, len(self.property_kv_ids))
        kvs = self.property_kv_ids
        for category in self:            
            if category.parent_id:
                kvs = kvs | category.parent_id.all_kvs
            else:
                _logger.debug("%s has no parent", category.name)
        _logger.debug("kvs count in %s : %s", self.name, len(self.property_kv_ids))
        self.all_kvs = kvs

    