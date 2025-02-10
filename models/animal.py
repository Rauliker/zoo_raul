from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import date

class ZooAnimal(models.Model):
    _name = "zoo.animal"

    name = fields.Char(required=True, string="Animal Name")
    date_birth = fields.Date(required=True, string="Date of birth")
    images = fields.Image(string="Images")
    gender = fields.Selection(
        string="Gender of the animal",
        selection=[('male', 'Male'), ('female', 'Female')]
    )
    food_type = fields.Selection(
        string="Food Type",
        selection=[
            ('herbivore', 'Herbivore'),
            ('carnivore', 'Carnivore'),
            ('omnivore', 'Omnivore'),
            ('frugivore', 'Frugivore'),
            ('piscivore', 'Piscivore'),
            ('insectivore', 'Insectivore'),
            ('folivore', 'Folivore'),
            ('nectarivore', 'Nectarivore'),
            ('granivore', 'Granivore')
        ],
        required=True
    )
    animal_country_id = fields.Many2one("res.country", "Animal country", required=True)
    animal_continent_id = fields.Many2one("zoo.continent", "Animal continent", required=True)
    age = fields.Integer(string="Age", compute="_compute_age", store=True)
    zoo_id = fields.Many2one("zoo.zoo", string="Zoo", required=True)
    species_id = fields.Many2one(
        "zoo.species", 
        string="Species", 
        required=True, 
        domain=[('id', '!=', False)], 
        ondelete="cascade"
    )
    status = fields.Selection(
        string="Status",
        selection=[('alive', 'Alive'), ('sick', 'Sick'), ('dead', 'Dead')],
        default='alive',
        required=True
    )
    date_of_death = fields.Date(string="Date of Death", store=True)

    @api.depends('date_birth', 'status', 'date_of_death')
    def _compute_age(self):
        for record in self:
            if record.status == 'dead' and record.date_of_death:
                death_date = fields.Date.from_string(record.date_of_death)
                birth_date = fields.Date.from_string(record.date_birth)
                record.age = (
                    death_date.year - birth_date.year
                    - ((death_date.month, death_date.day) < (birth_date.month, birth_date.day))
                )
            elif record.status == 'alive' and record.date_birth:
                today = date.today()
                birth_date = fields.Date.from_string(record.date_birth)
                record.age = (
                    today.year - birth_date.year
                    - ((today.month, today.day) < (birth_date.month, birth_date.day))
                )
            else:
                record.age = 0

    @api.constrains('date_birth')
    def _check_date_birth_is_valid(self):
        for record in self:
            if record.date_birth >= fields.Date.today():
                raise ValidationError("The date of birth must be earlier than today.")

    @api.onchange('status')
    def _onchange_status(self):
        if self.status == 'dead' and not self.date_of_death:
            self.date_of_death = fields.Date.today()

    def status_button(self):
        pass
