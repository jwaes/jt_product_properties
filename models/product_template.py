import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    property_kv_ids = fields.One2many('jt.property.kv', 'product_id', string='Property fields')
 