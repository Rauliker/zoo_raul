import uuid
from datetime import date
from odoo import fields, models, api

class ZooAnimal(models.Model):
    _name = "zoo.animal"
    
    id = fields.Char(
        required=True, 
        default=lambda self: str(uuid.uuid4()),
        readonly=True,
        index=True,
        copy=False
    )
    name = fields.Char(required=True, string="Animal Name")
    date = fields.Date(required=True, string="Date of birth")
    sexe = fields.Selection(
        string="Sex of the animal",
        selection=[
            ('male', 'Macho'),
            ('female', 'Hembra'),
        ]
    )
    animal_country_id = fields.Many2one(
        "res.country",
        "Animal country",
        required=True
    )
    age = fields.Integer(
        string="Age",
        compute="_compute_age",
        store=True
    )

    @api.depends('date')
    def _compute_age(self):
        for record in self:
            if record.date:
                today = date.today()
                birth_date = fields.Date.from_string(record.date)
                record.age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            else:
                record.age = 0