import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    tmpl_property_kv_ids = fields.One2many('jt.property.kv', 'product_template_id', string='Template Property fields')
    tmpl_all_kvs = fields.One2many('jt.property.kv', compute='_compute_all_kvs')

    @api.depends('tmpl_property_kv_ids')
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
 