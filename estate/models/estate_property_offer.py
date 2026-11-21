

from dateutil.relativedelta import relativedelta


from odoo import fields, models, api

class EstatePropertyOffer(models.Model):
    _name='estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    def accepted (self):
        if 'accepted' not in self.property_name.offer.mapped('status'):
            self.status = 'accepted'
        # if self.status == 'accepted':
            self.property_name.selling_price = self.price
            self.property_name.buyer=self.partner_id

        # for record in self:
        #     print(record.status)
        #     print(self.status)
        #     demo = record.mapped('price')
        #     # print(demo)


    def refused (self):
        self.status = 'refused'

    price=fields.Float(string='Price')
    status=fields.Selection([('accepted','Accepted'),('refused','Refused')],copy=False)
    partner_id=fields.Many2one('res.partner',string='Partner',required=True)
    property_name=fields.Many2one('estate.propertice',string='Property')
    validity=fields.Integer(string='Validity', default=7)
    date_deadline=fields.Datetime(string='Date of Deadline', compute='compute_deadline',inverse='compute_validity')
    property_type_id= fields.Many2one(related='property_name.property_type', string='Property Type id')

    @api.depends('create_date','validity')
    def compute_deadline (self):
        for record in self:
            if record.create_date:

                record.date_deadline = record.create_date + relativedelta(days=record.validity)
            else:
                print("hello")
                record.date_deadline=fields.Date.today() + relativedelta(days=record.validity)

    def compute_validity (self):
        for record in self:
                if record.create_date:
                    record.validity = (record.date_deadline - fields.Datetime.today()).days


    _check_price = models.Constraint(
        'CHECK( price >= 0 )',
        'price must be positive'
    )