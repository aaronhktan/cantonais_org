from unittest import TestCase

from ..utils import query_utils, default_settings


class TestConstructRomanizationQuery(TestCase):
    def test_empty(self):
        res = query_utils.construct_romanization_query([], "?")
        self.assertEqual(res, "")

        res = query_utils.construct_romanization_query([""], "?")
        self.assertEqual(res, "")

    def test_single_syllable(self):
        res = query_utils.construct_romanization_query(["se"], "?")
        self.assertEqual(res, "se?")

        res = query_utils.construct_romanization_query(["se2"], "?")
        self.assertEqual(res, "se2")

        res = query_utils.construct_romanization_query(["se*"], "?")
        self.assertEqual(res, "se*?")

        res = query_utils.construct_romanization_query(["se?"], "?")
        self.assertEqual(res, "se??")

    def test_multi_syllable(self):
        res = query_utils.construct_romanization_query(["se", "dak"], "?")
        self.assertEqual(res, "se? dak?")

        res = query_utils.construct_romanization_query(["se2", "dak1"], "?")
        self.assertEqual(res, "se2 dak1")

        res = query_utils.construct_romanization_query(["se*", "dak*"], "?")
        self.assertEqual(res, "se*? dak*?")

        res = query_utils.construct_romanization_query(["se?", "dak?"], "?")
        self.assertEqual(res, "se?? dak??")

    def test_glob_characters(self):
        res = query_utils.construct_romanization_query(["se", " *"], "?")
        self.assertEqual(res, "se? *")

        res = query_utils.construct_romanization_query(["se2", " ?", "?", "?"], "?")
        self.assertEqual(res, "se2 ???")

        res = query_utils.construct_romanization_query(
            ["se", " ?", "?", "? ", "dak"], "?"
        )
        self.assertEqual(res, "se? ??? dak?")

        res = query_utils.construct_romanization_query(["se", "*"], "?")
        self.assertEqual(res, "se*")

    def test_only_glob_characters(self):
        res = query_utils.construct_romanization_query(
            ["?", "?", "?", "?", "? ", "?", "?", "?", "?"], "?"
        )
        self.assertEqual(res, "????? ????")
