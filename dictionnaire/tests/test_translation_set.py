from unittest import TestCase

from ..models import TranslationSet


class TestGetSource(TestCase):
	def test_get_source(self):
		ts = TranslationSet(
			source="粵典—words.hk",
			translations=[])

		self.assertEqual(ts.source, "粵典—words.hk")