from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOfferModel(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float(
        string="Price"
    )

    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        copy=False
    )

    validity = fields.Integer(
        string="Validity",
        default=7
    )

    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline"
    )

    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
        required=True
    )

    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            create_date = (
                offer.create_date.date() if offer.create_date else fields.Date.today()
            )
            offer.date_deadline = create_date + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            create_date = (
                offer.create_date.date() if offer.create_date else fields.Date.today()
            )
            offer.validity = (
                (offer.date_deadline - create_date).days
                if offer.date_deadline else 0
            )

    def action_accept(self):
        for offer in self:
            accepted_offer = offer.property_id.offer_ids.filtered(
                lambda property_offer: (
                    property_offer.status == "accepted"
                    and property_offer != offer
                )
            )
            if accepted_offer:
                raise UserError("Only one offer can be accepted for a property.")

            offer.status = "accepted"
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.state = "offer_accepted"
        return True

    def action_refuse(self):
        for offer in self:
            offer.status = "refused"
        return True
