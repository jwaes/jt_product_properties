import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ProductProductProperties(models.Model):
    _inherit = ["product.product", "jt.property.mixin"]