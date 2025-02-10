import uuid
from datetime import date
from odoo import fields, models, api

class ZooSpecies(models.Model):
    _name = "zoo.species"
    _rec_name = "common_name"
    
    common_name = fields.Char(required=True, string="Common name")
    family = fields.Char(required=True, string="Family")
    scientific_name = fields.Char(required=True, string="Scientific name")
    profile = fields.Char(required=True, string="Profile")
    animal_id = fields.One2many(
        "zoo.animal",
        "species_id",
        string="Animal",
        required=True,
    )
    animal_count = fields.Integer(
        string="Animal Count",
        compute="_compute_animal_count",
        store=True
    )

    @api.depends('animal_id')
    def _compute_animal_count(self):
        for record in self:
            record.animal_count = len(record.animal_id)
    
    def __str__(self):
        return self.common_name