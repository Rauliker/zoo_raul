import uuid
from datetime import date
from odoo import fields, models, api

class ZooSpecies(models.Model):
    _name = "zoo.species"
    
    id = fields.Char(
        required=True, 
        default=lambda self: str(uuid.uuid4()),
        readonly=True,
        index=True,
        copy=False
    )
    family = fields.Char(required=True, string="Family")
    common_name = fields.Char(required=True, string="Common name")
    scientific_name = fields.Char(required=True, string="Scientific name")
    profile = fields.Char(required=True, string="Profile")
    animal_id = fields.One2many(
        "zoo.animal",
        "species_id",
        string="Animal",
        required=True,
    )