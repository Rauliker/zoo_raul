import uuid
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ZooEvent(models.Model):
    _name = 'zoo.event'
    _description = 'Zoo Event'
    _order = 'start_date asc'

    id = fields.Char(
        string="ID",
        required=True,
        default=lambda self: str(uuid.uuid4()),
        readonly=True,
        index=True,
        copy=False
    )

    name = fields.Char(string='Event Name', required=True)
    description = fields.Text(string='Description')
    start_date = fields.Datetime(string='Start Date', required=True)
    end_date = fields.Datetime(string='End Date', required=True)

    zoo_id = fields.Many2one(
        'zoo.zoo',
        string='Zoo',
        required=True,
        ondelete='cascade'
    )

    organizer_id = fields.Many2one(
        'res.partner',
        string='Organizer',
        required=True,
    )

    attendee_ids = fields.Many2many(
        'res.partner',
        string='Attendees'
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled')
    ], string='Status', default='draft')

    capacity = fields.Integer(string='Max Capacity', default=0)

    _sql_constraints = [
        ('check_date',
         'CHECK(end_date > start_date)',
         'The event end date must be after the start date.')
    ]

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for event in self:
            if event.start_date and event.end_date and event.end_date <= event.start_date:
                raise ValidationError("End Date must be after Start Date.")

    @api.constrains('capacity', 'attendee_ids')
    def _check_capacity(self):
        for event in self:
            if event.capacity > 0 and len(event.attendee_ids) > event.capacity:
                raise ValidationError("The number of attendees exceeds the event capacity.")

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_complete(self):
        self.write({'state': 'completed'})

    def action_cancel(self):
        self.write({'state': 'canceled'})

    @api.model
    def check_event_status(self):
        today = fields.Datetime.now()
        for event in self.search([('state', '!=', 'canceled')]):
            if event.end_date and event.end_date < today:
                event.write({'state': 'completed'})
