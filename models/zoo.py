import uuid
from odoo import fields, models

class Zoo(models.Model):
    _name = "zoo.zoo"
    
    id = fields.Char(
        required=True, 
        default=lambda self: str(uuid.uuid4()),
        readonly=True,
        index=True,
        copy=False
    )
    name = fields.Char(required=True, string="Zoo's Name")
    size = fields.Integer(required=True, string="Zoo's Size")
    country_id = fields.Many2one(
        "res.country",
        "Country",
        required=True
    ) 
    city_id = fields.Many2one(
        "res.city", 
        string="City",
        required=True,
    )

