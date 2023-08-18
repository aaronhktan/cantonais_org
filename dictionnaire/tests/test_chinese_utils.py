from unittest import TestCase

from ..utils import chinese_utils, default_settings


class TestExtractJyutpingTones(TestCase):
    def test_simple(self):
        string = "zeng3 je5"
        res = chinese_utils.extract_jyutping_tones(string)
        self.assertEqual(res, [3, 5])

    def test_no_spaces(self):
        string = "zeng3je5"
        res = chinese_utils.extract_jyutping_tones(string)
        self.assertEqual(res, [3, 5])


class TestExtractPinyinTones(TestCase):
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


class TestCompareStrings(TestCase):
    def test_simple(self):
        res = chinese_utils.compare_strings("語言藝術", "语言艺术")
        self.assertEqual(res, "语－艺术")

    def test_single_multibyte_grapheme(self):
        res = chinese_utils.compare_strings("賵", "赗")
        self.assertEqual(res, "赗")

    def test_multiple_multibyte_graphemes(self):
        res = chinese_utils.compare_strings("齮齕", "𬺈龁")
        self.assertEqual(res, "𬺈龁")

    def test_multibyte_graphemes_with_alpha(self):
        res = chinese_utils.compare_strings("齮aaaa齕", "𬺈aaaa龁")
        self.assertEqual(res, "𬺈－－－－龁")

    def test_compatibility_variant_normalization(self):
        res = chinese_utils.compare_strings("響", "響")
        self.assertEqual(res, "－")


class TestJyutpingToYale(TestCase):
    def test_simple(self):
        res = chinese_utils.jyutping_to_yale("si1 zi2 saan1")
        self.assertEqual(res, "sī jí sāan")

    def test_no_spaces(self):
        res = chinese_utils.jyutping_to_yale("si1zi2saan1")
        self.assertEqual(res, "sī jí sāan")

    def test_spaces_to_segment(self):
        res = chinese_utils.jyutping_to_yale(
            "si1 zi2 saan1", use_spaces_to_segment=True)
        self.assertEqual(res, "sī jí sāan")

    def test_special_final(self):
        res = chinese_utils.jyutping_to_yale("goek3jyun5")
        self.assertEqual(res, "geuk yúhn")

    def test_light_tone(self):
        res = chinese_utils.jyutping_to_yale("lok6 jyu5")
        self.assertEqual(res, "lohk yúh")

    def test_special_syllable(self):
        res = chinese_utils.jyutping_to_yale("m4 hai6")
        self.assertEqual(res, "m̀h haih")

    def test_no_tone(self):
        res = chinese_utils.jyutping_to_yale("mit")
        self.assertEqual(res, "mit")


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
