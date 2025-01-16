import uuid
from odoo import fields, models

class ZooAnimal(models.Model):
    _name = "zoo.aminal"
    
    id = fields.Char(
        required=True, 
        default=lambda self: str(uuid.uuid4()),
        readonly=True,
        index=True,
        copy=False
    )
    name = fields.Char(required=True, string="Animal Name"),
    date = fields.Date(required=True, string="Date of birth"),
    sexe = fields.Selection(
        string="Sex of the animal",
        selection=[
            ('male', 'Macho'),
            ('female ', 'Hembra'),
        ]
    )
    animal_country_id = fields.Many2one(
        "res.country",
        "Animal country",
        required=True
    )
    