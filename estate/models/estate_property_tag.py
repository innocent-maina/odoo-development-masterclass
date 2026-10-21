from odoo import models, fields

class EstatePropertyTagModel(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property tag"

    name = fields.Char('Name', required=True)