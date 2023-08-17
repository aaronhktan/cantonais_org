from unittest import TestCase

from ..utils import chinese_utils, default_settings


class TestApplyJyutpingTones(TestCase):
    def test_simple(self):
        string = "zeng3 je5"
        res = chinese_utils.extract_jyutping_tones(string)
        self.assertEqual(res, [3, 5])

    def test_no_spaces(self):
        string = "zeng3je5"
        res = chinese_utils.extract_jyutping_tones(string)
        self.assertEqual(res, [3, 5])


class TestApplyPinyinTones(TestCase):
    def test_simple(self):
        string = "xiang1 gang3"
        res = chinese_utils.extract_pinyin_tones(string)
        self.assertEqual(res, [1, 3])

    def test_no_spaces(self):
        string = "xiang1gang3"
        res = chinese_utils.extract_pinyin_tones(string)
        self.assertEqual(res, [1, 3])


class TestApplyColours(TestCase):
    def test_jyutping(self):
        string = "唔係"
        tones = [4, 6]
        res = chinese_utils.apply_colours(
            string, tones, default_settings.DEFAULT_JYUTPING_TONES)
        self.assertEqual(
            res, (f"<span style=\"color: "
                  f"{default_settings.DEFAULT_JYUTPING_TONES[4]}\">唔</span>"
                  f"<span style=\"color: "
                  f"{default_settings.DEFAULT_JYUTPING_TONES[6]}\">係</span>"))

    def test_pinyin(self):
        string = "不是"
        tones = [2, 4]
        res = chinese_utils.apply_colours(
            string, tones, default_settings.DEFAULT_PINYIN_TONES)
        self.assertEqual(
            res, (f"<span style=\"color: "
                  f"{default_settings.DEFAULT_PINYIN_TONES[2]}\">不</span>"
                  f"<span style=\"color: "
                  f"{default_settings.DEFAULT_PINYIN_TONES[4]}\">是</span>"))


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

    def test_lower(self):
        res = chinese_utils.segment_jyutping(
            "mGoI")
        self.assertEqual(res, ["m", "goi"])

    def test_lower_with_digits(self):
        res = chinese_utils.segment_jyutping(
            "m4GoI1")
        self.assertEqual(res, ["m4", "goi1"])

    def test_multiple_finals_vowels_only(self):
        res = chinese_utils.segment_jyutping("aaaa")
        self.assertEqual(res, ["aa", "aa"])

    def test_multiple_finals_consonants_only(self):
        res = chinese_utils.segment_jyutping("ngng")
        self.assertEqual(res, ["ng", "ng"])

    def test_multiple_finals(self):
        res = chinese_utils.segment_jyutping("amam")
        self.assertEqual(res, ["am", "am"])

    def test_garbage(self):
        res = chinese_utils.segment_jyutping(
            "kljnxclkjvnl")
        self.assertEqual(res, ["kljnxclkjvnl"])


class TestPinyinSegmentation(TestCase):
    def test_simple(self):
        res = chinese_utils.segment_pinyin("guang3 dong1")
        self.assertEqual(res, ["guang3", "dong1"])

    def test_no_digits(self):
        res = chinese_utils.segment_pinyin("guang dong")
        self.assertEqual(res, ["guang", "dong"])

    def test_no_spaces(self):
        res = chinese_utils.segment_pinyin("guang3dong1")
        self.assertEqual(res, ["guang3", "dong1"])

    def test_no_digits_no_spaces(self):
        res = chinese_utils.segment_pinyin("guangdong")
        self.assertEqual(res, ["guang", "dong"])

    def test_no_digits_apostrophe(self):
        res = chinese_utils.segment_pinyin("xi'an")
        self.assertEqual(res, ["xi", "an"])

    def test_digits_apostrophe(self):
        res = chinese_utils.segment_pinyin("xi1'an")
        self.assertEqual(res, ["xi1", "an"])

    def test_remove_special_characters(self):
        res = chinese_utils.segment_pinyin("guang*dong!!")
        self.assertEqual(res, ["guang", "dong"])

    def test_keep_glob_characters(self):
        res = chinese_utils.segment_pinyin(
            "guang* dong?", remove_glob_characters=False)
        self.assertEqual(res, ["guang", "* ", "dong", "?"])

    def test_keep_glob_characters_no_whitespace(self):
        res = chinese_utils.segment_pinyin(
            "guang*dong?", remove_glob_characters=False)
        self.assertEqual(res, ["guang", "*", "dong", "?"])

    def test_keep_multiple_glob_characters(self):
        res = chinese_utils.segment_pinyin(
            "guang?* dong", remove_glob_characters=False)
        self.assertEqual(res, ["guang", "?", "* ", "dong"])

    def test_keep_multiple_glob_characters_whitespace(self):
        res = chinese_utils.segment_pinyin(
            "guang? * dong", remove_glob_characters=False)
        self.assertEqual(res, ["guang", "? ", "* ", "dong"])

    def test_keep_multiple_glob_characters_whitespace_surround(self):
        res = chinese_utils.segment_pinyin(
            "guang ? * dong", remove_glob_characters=False)
        self.assertEqual(res, ["guang", " ? ", "* ", "dong"])

    def test_glob_characters_trim_whitespace(self):
        res = chinese_utils.segment_pinyin(
            "guang  ?            *      dong", remove_glob_characters=False)
        self.assertEqual(res, ["guang", " ? ", "* ", "dong"])

    def test_keep_special_characters(self):
        res = chinese_utils.segment_pinyin(
            "guang？ dong1", remove_special_characters=False)
        self.assertEqual(res, ["guang", "？", "dong1"])

    def test_remove_whitespace(self):
        res = chinese_utils.segment_pinyin(
            "  guang                           dong      ")
        self.assertEqual(res, ["guang", "dong"])

    def test_lower(self):
        res = chinese_utils.segment_pinyin(
            "gUanGdOnG")
        self.assertEqual(res, ["guang", "dong"])

    def test_lower_with_digits(self):
        res = chinese_utils.segment_pinyin(
            "guAng3dONg1")
        self.assertEqual(res, ["guang3", "dong1"])

    def test_multiple_finals_vowels_only(self):
        res = chinese_utils.segment_pinyin("ee")
        self.assertEqual(res, ["e", "e"])

    def test_multiple_finals(self):
        res = chinese_utils.segment_pinyin("angang")
        self.assertEqual(res, ["ang", "ang"])

    def test_garbage(self):
        res = chinese_utils.segment_pinyin(
            "kljnxclkjvnl")
        self.assertEqual(res, ["kljnxclkjvnl"])
