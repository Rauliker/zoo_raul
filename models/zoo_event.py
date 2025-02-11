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

    @api.onchange('attendee_ids')
    def _onchange_attendee_ids(self):
        for event in self:
            if event.capacity > 0 and len(event.attendee_ids) > event.capacity:
                raise ValidationError("Cannot add more attendees. Event is at full capacity.")

    def write(self, vals):
        if 'attendee_ids' in vals:
            new_attendees = vals.get('attendee_ids', [])
            if isinstance(new_attendees, list) and any(op[0] in (0, 4) for op in new_attendees):
                total_attendees = len(self.attendee_ids) + sum(1 for op in new_attendees if op[0] in (0, 4))
                if self.capacity > 0 and total_attendees > self.capacity:
                    raise ValidationError("Cannot add more attendees. Event is at full capacity.")
        return super(ZooEvent, self).write(vals)

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
