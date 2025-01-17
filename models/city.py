from odoo import models, fields

class City(models.Model):
    _name = 'zoo.city'
    _description = 'City'

    name = fields.Char(string='City Name', required=True)
    country_id = fields.Many2one('res.country', string='Country', required=True)
