import unittest

from afmt import Formatter


class FormatterTest(unittest.TestCase):
	def setUp(self):
		self.f = Formatter()

	def test_inline_specs(self):
		f = self.f
		string = f'{f:b i u goto(5,6)}hello{f:e}'

		self.assertIn('\033[0m', string)
		self.assertIn('\033[1m', string)
		self.assertIn('\033[3m', string)
		self.assertIn('\033[4m', string)
		self.assertIn('\033[5;6H', string)
		self.assertIn('hello', string)

	def test_init_style(self):
		f = Formatter({'custom_style': 'b fg(255,0,127)'})
		string = f'{f:i custom_style}hello{f:e}'

		self.assertIn('\033[0m', string)
		self.assertIn('\033[1m', string)
		self.assertIn('\033[3m', string)
		self.assertIn('\033[38;2;255;0;127m', string)

	def test_add_style(self):
		self.f.add_style('custom_style', 'b fg(255,0,127)')
		f = self.f
		string = f'{f:i custom_style}hello{f:e}'

		self.assertIn('\033[0m', string)
		self.assertIn('\033[1m', string)
		self.assertIn('\033[3m', string)
		self.assertIn('\033[38;2;255;0;127m', string)
