from unittest import TestCase

from ..utils import chinese_utils


class TestJyutpingSegmentation(TestCase):
    def test_simple(self):
        res = chinese_utils.segment_jyutping("m4 goi1")
        self.assertEqual(res, ["m4", "goi1"])

    def test_no_digits(self):
        res = chinese_utils.segment_jyutping("m goi")
        self.assertEqual(res, ["m", "goi"])

    def test_no_spaces(self):
        res = chinese_utils.segment_jyutping("m4goi1")
        self.assertEqual(res, ["m4", "goi1"])

    def test_no_digits_no_spaces(self):
        res = chinese_utils.segment_jyutping("mgoi")
        self.assertEqual(res, ["m", "goi"])

    def test_no_digits_apostrophe(self):
        res = chinese_utils.segment_jyutping("m'aam")
        self.assertEqual(res, ["m", "aam"])

    def test_digits_apostrophe(self):
        res = chinese_utils.segment_jyutping("m4'aam")
        self.assertEqual(res, ["m4", "aam"])

    def test_remove_special_characters(self):
        res = chinese_utils.segment_jyutping("m*goi")
        self.assertEqual(res, ["m", "goi"])

    def test_keep_glob_characters(self):
        res = chinese_utils.segment_jyutping(
            "m* goi", remove_glob_characters=False)
        self.assertEqual(res, ["m", "* ", "goi"])

    def test_keep_glob_characters_no_whitespace(self):
        res = chinese_utils.segment_jyutping(
            "m*goi", remove_glob_characters=False)
        self.assertEqual(res, ["m", "*", "goi"])

    def test_keep_multiple_glob_characters(self):
        res = chinese_utils.segment_jyutping(
            "m?* goi", remove_glob_characters=False)
        self.assertEqual(res, ["m", "?", "* ", "goi"])

    def test_keep_multiple_glob_characters_whitespace(self):
        res = chinese_utils.segment_jyutping(
            "m? * goi", remove_glob_characters=False)
        self.assertEqual(res, ["m", "? ", "* ", "goi"])

    def test_keep_multiple_glob_characters_whitespace_surround(self):
        res = chinese_utils.segment_jyutping(
            "m ? * goi", remove_glob_characters=False)
        self.assertEqual(res, ["m", " ? ", "* ", "goi"])
    
    def test_glob_characters_trim_whitespace(self):
        res = chinese_utils.segment_jyutping(
            "m  ?            *      goi", remove_glob_characters=False)
        self.assertEqual(res, ["m", " ? ", "* ", "goi"])

    def test_keep_special_characters(self):
        res = chinese_utils.segment_jyutping(
            "m？ goi", remove_special_characters=False)
        self.assertEqual(res, ["m", "？", "goi"])

    def test_remove_whitespace(self):
        res = chinese_utils.segment_jyutping(
            "  m                           goi      ")
        self.assertEqual(res, ["m", "goi"])

    def test_garbage(self):
        res = chinese_utils.segment_jyutping(
            "kljnxclkjvnl")
        self.assertEqual(res, ["kljnxclkjvnl"])
