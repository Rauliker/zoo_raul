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
    size = fields.Integer(required=True, string="Zoo's Size(sqm)")
    country_id = fields.Many2one(
        "res.country",
        "Country",
        required=True
    ) 
    city_id = fields.Many2one(
        "zoo.city", 
        string="City",
        required=True,
    )
    animal_id = fields.One2many(
        "zoo.animal",
        "zoo_id",
        string="Animal",
        required=True,
    )
    @api.onchange('city_id')
    def _onchange_city_id(self):
        if self.city_id:
            self.country_id = self.city_id.country_id
        else:
            self.country_id = False

    @api.constrains('city_id', 'country_id')
    def _check_city_country_relation(self):
        for record in self:
            if record.city_id and record.city_id.country_id != record.country_id:
                raise ValidationError(
                    f"The city '{record.city_id.name}' does not belong to the country '{record.country_id.name}'."
                )

    @api.constrains('size')
    def _check_size_is_bigger_than_zero(self):
        for record in self:
            if record.size <= 0:
                raise ValidationError(
                    "Size must be greater than 0."
                )
