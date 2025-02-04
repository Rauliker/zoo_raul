import uuid
from odoo import api, fields, models
from odoo.exceptions import ValidationError

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
    size = fields.Integer(required=True, string="Zoo's Size (sqm)")
    
    country_id = fields.Many2one(
        "res.country",
        string="Country",
        required=True
    )
    
    provincia_id = fields.Many2one(
        "res.country.state",
        string="Province",
        required=True,
        domain="[('country_id', '=', country_id)]"
    )
    
    city_name = fields.Char(
        string="City",
        required=True
    )
    
    animal_id = fields.One2many(
        "zoo.animal",
        "zoo_id",
        string="Animal",
        required=True,
    )

    @api.onchange('provincia_id')
    def _onchange_provincia_id(self):
        if self.provincia_id:
            self.country_id = self.provincia_id.country_id

    @api.constrains('size')
    def _check_size_is_bigger_than_zero(self):
        for record in self:
            if record.size <= 0:
                raise ValidationError("Size must be greater than 0.")
