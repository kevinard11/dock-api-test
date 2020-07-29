from django.test import TestCase
from app.calc import add,substract
class CalcTests(TestCase):
    def test_add(self):
        """Test add"""
        self.assertEqual(add(3, 8), 11)
    def test_substract(self):
        """Test substract"""
        self.assertEqual(substract(3, 8), -5)
