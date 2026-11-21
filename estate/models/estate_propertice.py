from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo import models, fields, api
class Propertice(models.Model):
    _name = 'estate.propertice'
    _description = 'Property'




    def cancel(self):
        if self.state != 'sold':
            self.state = 'cancelled'
        else:
            raise UserError("""Sold product can't be canceled""")

    def sold(self):
        if self.state != 'cancelled':
            self.state = 'sold'
        else:
            raise UserError("""Canceled product can't be sold""")





    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    description = fields.Text()
    postcode = fields.Char()
    date_available = fields.Date( copy=False, help="Date available", default=fields.Date.today()+relativedelta(months=+3))
    expected_price= fields.Float(required=True)
    selling_price = fields.Float( readonly=True )
    beadroom=fields.Integer(default=2)
    garden= fields.Boolean( onchage='garden_onchage')
    garden_orientation= fields.Selection( selection=[('North','north'), ('South','south'), ('East','east'), ('West','west')])




    living_area=fields.Float()
    garden_area=fields.Float()
    total_area = fields.Float(compute='compute_total_area')
    @api.depends('living_area','garden_area')
    def compute_total_area(self):
        for record in self:
            record.total_area=record.living_area + record.garden_area





    best_price = fields.Float(compute='compute_offer_price')
    @api.depends('offer.price')
    def compute_offer_price(self):
        for record in self:
            print(record.offer.mapped('price'))
            record.best_price=max(record.offer.mapped('price'),default=0)

    # @api.depends('offer')
    # def compute_property_type(self):
    #     self.offer.property_type_id = self.property_type

    area= fields.Float(readonly=True)
    state= fields.Selection(selection=[('new','New'),('offer received','Offer received'),('offer accepted','Offer accepted'),('sold','Sold'),('cancelled','Cancelled')],default='new')
    property_type= fields.Many2one('estate.property.type', string='Property Type')
    salesman= fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.company.id)
    buyer = fields.Many2one('res.partner', string='Buyer', copy=False)
    tag=fields.Many2many('estate.property.tag', string='Tag')
    offer=fields.One2many('estate.property.offer','property_name', string='Offer')

    # @api.depends('offer')
    # def onchange_offer(self):
    #     for record in self:
    #         if record.offer == 'new':
    #             record.state = 'offer accepted'


    @api.onchange('garden')
    def garden_onchage(self):
        for record in self:
            if record.garden:
                record.garden_area=10
                record.garden_orientation= 'North'
            else:
                record.garden_area=0
                record.garden_orientation= None


    _check_expected = models.Constraint(
        'CHECK( expected_price >= 0 )',
        'expected must be positive'
    )
    _check_selling_price = models.Constraint(
        'CHECK( selling_price >= 0 )',
        'selling price must be positive'
    )

    @api.constrains('expected_price','selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price :
                if record.selling_price <= record.expected_price*90/100:
                    raise UserError("""The selling Price atleaste 90% of expected price!""")


    @api.ondelete(at_uninstall=False)
    def delete_property(self):
        for record in self:
            if record.state not in ['new','cancelled']:
                raise UserError(f'{record.state} property cannot be deleted')