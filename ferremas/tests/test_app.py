import unittest
from app import Product

class TestProductModel(unittest.TestCase):

    def test_create_product_success(self):
        # Prueba de creación de producto exitosa
        product = Product('Test Product', 100)
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.price, 100)

    def test_create_product_negative_price(self):
        # Prueba de creación de producto con precio negativo
        with self.assertRaises(ValueError):
            Product('Test Product', -50)

    def test_apply_discount_success(self):
        # Prueba de aplicación de descuento exitosa
        product = Product('Test Product', 100)
        product.apply_discount(0.1)
        self.assertEqual(product.price, 90)

    def test_apply_discount_invalid(self):
        # Prueba de aplicación de descuento inválido
        product = Product('Test Product', 100)
        with self.assertRaises(ValueError):
            product.apply_discount(1.5)

if __name__ == '__main__':
    unittest.main()
