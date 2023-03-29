import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class ProductCategory(models.Model):
    _inherit = 'product.category'

    property_kv_ids = fields.One2many('jt.property.kv', 'category_id', string='Property fields')
    all_kvs = fields.One2many('jt.property.kv', compute='_compute_all_kvs', recursive=True,)

    @api.depends('property_kv_ids','parent_id','parent_id.all_kvs')
    def _compute_all_kvs(self):
        for categ in self:

            kvs = categ.property_kv_ids

            all_parental_kvs = self.env['jt.property.kv']

            if categ.parent_id:
                all_parental_kvs = categ.parent_id.all_kvs
            _logger.debug("all_parental_kvs length for %s is %s", categ.name, len(all_parental_kvs))

            for kv in categ.property_kv_ids:
                #looking for values in parental map to remove
                if kv.key_id.behavior == 'replace':
                    all_parental_kvs = all_parental_kvs.filtered(lambda kvi: kvi.code != kv.code)
            _logger.debug("after filtering, all_parental_kvs length for %s is %s", categ.name, len(all_parental_kvs))

            #now merging new values
            categ.all_kvs = all_parental_kvs | categ.property_kv_ids
            _logger.debug("final all kvs count in %s : %s", categ.name, len(categ.all_kvs))

            # _logger.info("┌──[CAT] %s ", categ.name)
            # for kvl in categ.all_kvs:
            #     _logger.info("├─ %s : %s", kvl.code, kvl.text)