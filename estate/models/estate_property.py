from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstateModel(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(
        string="Name of Property",
        required=True
    )

    description = fields.Text(
        string="Description of Property"
    )

    postcode = fields.Char(
        string="Postcode"
    )

    date_availability = fields.Date(
        string="Date Available",
        default=lambda self: fields.Date.today() + relativedelta(months=3),
        copy=False
    )

    expected_price = fields.Float(
        string="Expected Price",
        required=True
    )

    selling_price = fields.Float(
        string="Selling Price",
        readonly=True,
        copy=False
    )

    best_price = fields.Float(
        string="Best Offer",
        compute="_compute_best_price"
    )

    bedrooms = fields.Integer(
        string="# of Bedrooms",
        required=True,
        default=2
    )

    living_area = fields.Integer(
        string="Living Area"
    )

    facades = fields.Integer(
        string="Facades"
    )

    garden = fields.Boolean(
        string="Has Garden"
    )

    garage = fields.Boolean(
        string="Has Garage"
    )

    garden_area = fields.Integer(
        string="Garden Area"
    )

    total_area = fields.Integer(
        string="Total Area",
        compute="_compute_total_area"
    )

    active = fields.Boolean(
        string="Active",
        default=True
    )

    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="new"
    )

    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        string="Type"
    )

    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type"
    )

    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False
    )

    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user
    )

    tag_ids = fields.Many2many(
        "estate.property.tag",
        string="Tags"
    )

    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers"
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property_record in self:
            property_record.total_area = (
                property_record.living_area + property_record.garden_area
            )

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for property_record in self:
            property_record.best_price = max(
                property_record.offer_ids.mapped("price"),
                default=0.0
            )

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self):
        for property_record in self:
            if property_record.state == "canceled":
                raise UserError("Canceled properties cannot be sold.")
            property_record.state = "sold"
        return True

    def action_cancel(self):
        for property_record in self:
            if property_record.state == "sold":
                raise UserError("Sold properties cannot be canceled.")
            property_record.state = "canceled"
        return True
