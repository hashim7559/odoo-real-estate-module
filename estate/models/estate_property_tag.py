from odoo import fields, models
class EstatePropertyTag(models.Model):
    _name='estate.property.tag'
    _description='propert tag'
    _order='name'

    name=fields.Char(string='Tag')
    color=fields.Integer(string='Color')
    _tag_unique=models.Constraint(
        'Unique(name)',
        'Tag name must be unique'
    )
