from odoo import models, fields

class Continent(models.Model):
    _name = 'zoo.continent'
    _description = 'Continent'

    name = fields.Char(string='Continent Name', required=True)
    country_ids = fields.One2many('res.country', 'continent_id', string='Countries')

class ResCountry(models.Model):
    _inherit = 'res.country'

    continent_id = fields.Many2one('zoo.continent', string='Continent')
