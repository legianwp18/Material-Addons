from odoo import fields
from odoo.tests import new_test_user
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestProductMaterial(TransactionCase):

    def setUp(self):
        super(TestProductMaterial, self).setUp()
        self.Material = self.env['product.material']
        self.company = self.env.ref("base.main_company")
        self.supplier = (
            self.env["res.partner"]
                .with_context(tracking_disable=True)
                .create(
                {
                    "name": "supplier1",
                    "phone": "123",
                }
            )
        )

    def test_create_material(self):
        material_data = {
            "name": "Test Material",
            "material_code": "MC123",
            "material_type": "Fabric",
            "material_buy_price": 100000,
            "supplier_id": self.supplier.id,
            "company_id": self.company.id
        }
        new_material = self.Material.create(material_data)
        self.assertTrue(new_material, "Material creation failed")
        self.assertEqual(new_material.name, 'Test Material', "Material name mismatch")

    def test_material_buy_price(self):
        material_data = {
            "name": "Test Material",
            "material_code": "MC123",
            "material_type": "Fabric",
            "material_buy_price": 20,
            "supplier_id": self.supplier.id,
            "company_id": self.company.id
        }
        with self.assertRaises(UserError):
            new_material = self.Material.create(material_data)
            self.assertFalse(new_material, "Validation material_buy_price failed")

    def test_update_material(self):
        material = self.Material.create({
            "name": "Test Material 2",
            "material_code": "MC1234",
            "material_type": "Fabric",
            "material_buy_price": 100000,
            "supplier_id": self.supplier.id,
            "company_id": self.company.id
        })
        material.write({'material_buy_price': 200000})
        self.assertEqual(material.material_buy_price, 200000, "Material price updated")

    def test_delete_material(self):
        material = self.Material.create({
            "name": "Test Material 3",
            "material_code": "MC12345",
            "material_type": "Fabric",
            "material_buy_price": 100000,
            "supplier_id": self.supplier.id,
            "company_id": self.company.id
        })
        material.unlink()
        deleted_product = self.Material.search([('id', '=', material.id)])
        self.assertFalse(deleted_product, "Material deletion failed")