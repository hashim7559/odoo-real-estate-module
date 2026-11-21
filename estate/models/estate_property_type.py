
from odoo import models, fields,api

class EstatePropertyType(models.Model):

    _name = 'estate.property.type'
    _description = 'Estate Property Types'
    _order = 'name'

    def offer_button(self):
        return

    name = fields.Char(required=True)
    sequence =fields.Integer()
    property_name = fields.One2many('estate.propertice', 'property_type')
    offer_id=fields.One2many('estate.property.offer', 'property_type_id')
    offer_count=fields.Integer(compute='compute_offer_count')

    @api.depends('offer_id')
    def compute_offer_count(self):
        for offer in self:
            offer.offer_count = len(offer.offer_id)


    _property_type_unique=models.Constraint(
        'Unique(name)',
        'Property type must be unique'
    )