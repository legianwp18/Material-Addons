from odoo import fields, models, api, _
from odoo.exceptions import UserError


class ProductMaterial(models.Model):
    _name = 'product.material'
    _description = 'Product Material'

    name = fields.Char(
        string='Name',
        required=True)

    material_code = fields.Char(
        string="Material Code",
        index=True,
        required=True)

    material_type = fields.Selection(
        string="Material Type",
        selection=[
            ('Fabric', 'Fabric'),
            ('Jeans', 'Jeans'),
            ('Cotton', 'Cotton')
        ], required=True )

    material_buy_price = fields.Float(
        string='Material Buy Price',
        digits='Material Price',
        required=True )

    supplier_id = fields.Many2one(
        comodel_name='res.partner',
        string="Related Supplier",
        required=True )

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company)

    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        store=True, readonly=False,
        compute='_compute_currency_id')

    @api.onchange('material_buy_price')
    def _onchange_standard_price(self):
        if self.material_buy_price < 100 and self.material_buy_price > 0 :
            raise UserError('The material buy price cannot be less than 100.')

    @api.depends('company_id')
    def _compute_currency_id(self):
        main_company = self.env['res.company']._get_main_company()
        for rec in self:
            rec.currency_id = rec.company_id.sudo().currency_id.id or main_company.currency_id.id

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            standard_price = vals.get("material_buy_price", False)
            if standard_price and standard_price < 100:
                raise UserError('The material buy price cannot be less than 100.')
        return super(ProductMaterial, self).create(vals_list)

    def write(self, values):
        standard_price = values.get("material_buy_price", False)
        if standard_price and standard_price < 100:
            raise UserError('The material buy price cannot be less than 100.')
        return super(ProductMaterial, self).write(values)