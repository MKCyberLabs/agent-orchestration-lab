import unittest

from sample_app.calculator import add


class CalculatorTests(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)

    def test_add_negative(self):
        self.assertEqual(add(-2, 5), 3)


if __name__ == "__main__":
    unittest.main()
