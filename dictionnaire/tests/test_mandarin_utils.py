from unittest import TestCase

from ..utils import mandarin_utils


class TestExtractPinyinTones(TestCase):
    def test_simple(self):
        string = "xiang1 gang3"
        res = mandarin_utils.extract_pinyin_tones(string)
        self.assertEqual(res, [1, 3])

    def test_no_spaces(self):
        string = "xiang1gang3"
        res = mandarin_utils.extract_pinyin_tones(string)
        self.assertEqual(res, [1, 3])

    def test_bad_numeric(self):
        string = "㒃"
        res = mandarin_utils.extract_pinyin_tones(string)
        self.assertEqual(res, [])


class TestPrettyPinyin(TestCase):
    def test_simple(self):
        res = mandarin_utils.pretty_pinyin("shuai4 ge1")
        self.assertEqual(res, "shuài gē")

    def test_reject_no_tone(self):
        res = mandarin_utils.pretty_pinyin("ba")
        self.assertEqual(res, "ba")

    def test_reject_single_letter(self):
        res = mandarin_utils.pretty_pinyin("a")
        self.assertEqual(res, "a")

    def test_reject_special_character(self):
        res = mandarin_utils.pretty_pinyin("-")
        self.assertEqual(res, "-")

    def test_secondary_vowel(self):
        res = mandarin_utils.pretty_pinyin("hui4 tu2")
        self.assertEqual(res, "huì tú")

    def test_umlaut(self):
        res = mandarin_utils.pretty_pinyin("nu:3 hai2")
        self.assertEqual(res, "nǚ hái")

    def test_tones(self):
        res = mandarin_utils.pretty_pinyin("ma1 ma2 ma3 ma4")
        self.assertEqual(res, "mā má mǎ mà")

    def test_no_tone(self):
        res = mandarin_utils.pretty_pinyin("nu")
        self.assertEqual(res, "nu")


class TestNumberedPinyin(TestCase):
    def test_simple(self):
        res = mandarin_utils.numbered_pinyin("nu:3 hai2")
        self.assertEqual(res, "nü3 hai2")


class TestPinyinWithV(TestCase):
    def test_simple(self):
        res = mandarin_utils.pinyin_with_v("nu:3 hai2")
        self.assertEqual(res, "nv3 hai2")


class TestPinyinToZhuyin(TestCase):
    def test_simple(self):
        res = mandarin_utils.pinyin_to_zhuyin("ba1 da2 tong1")
        self.assertEqual(res, "ㄅㄚ ㄉㄚˊ ㄊㄨㄥ")

    def test_reject_no_tone(self):
        res = mandarin_utils.pinyin_to_zhuyin("ba")
        self.assertEqual(res, "ba")

    def test_reject_single_letter(self):
        res = mandarin_utils.pinyin_to_zhuyin("a")
        self.assertEqual(res, "a")

    def test_reject_special_character(self):
        res = mandarin_utils.pinyin_to_zhuyin("-")
        self.assertEqual(res, "-")

    def test_no_spaces(self):
        res = mandarin_utils.pinyin_to_zhuyin("ba1da2tong1")
        self.assertEqual(res, "ㄅㄚ ㄉㄚˊ ㄊㄨㄥ")

    def test_use_spaces_to_segment(self):
        res = mandarin_utils.pinyin_to_zhuyin(
            "ba1 da2 tong1", use_spaces_to_segment=True
        )
        self.assertEqual(res, "ㄅㄚ ㄉㄚˊ ㄊㄨㄥ")

    def test_special_initials(self):
        res = mandarin_utils.pinyin_to_zhuyin("qu4")
        self.assertEqual(res, "ㄑㄩˋ")

        res = mandarin_utils.pinyin_to_zhuyin("chi1")
        self.assertEqual(res, "ㄔ")

        res = mandarin_utils.pinyin_to_zhuyin("ri4")
        self.assertEqual(res, "ㄖˋ")

    def test_special_finals(self):
        res = mandarin_utils.pinyin_to_zhuyin("hm5")
        self.assertEqual(res, "˙ㄏㄇ")

        res = mandarin_utils.pinyin_to_zhuyin("hng5")
        self.assertEqual(res, "˙ㄏㄫ")

        res = mandarin_utils.pinyin_to_zhuyin("er2")
        self.assertEqual(res, "ㄦˊ")

    def test_erhua(self):
        res = mandarin_utils.pinyin_to_zhuyin("quanr1")
        self.assertEqual(res, "ㄑㄩㄢㄦ")

    def test_malformed(self):
        res = mandarin_utils.pinyin_to_zhuyin("chzng2 quanr1")
        self.assertEqual(res, "ㄔzng2 ㄑㄩㄢㄦ")


class TestPinyinToIPA(TestCase):
    def test_simple(self):
        res = mandarin_utils.pinyin_to_IPA("ba1 da2 tong1")
        self.assertEqual(res, "pä˥˥ tä˧˥ tʰʊŋ˥˥")

    def test_reject_no_tone(self):
        res = mandarin_utils.pinyin_to_IPA("ba")
        self.assertEqual(res, "ba")

    def test_reject_single_letter(self):
        res = mandarin_utils.pinyin_to_IPA("a")
        self.assertEqual(res, "a")

    def test_reject_special_character(self):
        res = mandarin_utils.pinyin_to_IPA("-")
        self.assertEqual(res, "-")

    def test_no_spaces(self):
        res = mandarin_utils.pinyin_to_IPA("ba1da2tong1")
        self.assertEqual(res, "pä˥˥ tä˧˥ tʰʊŋ˥˥")

    def test_use_spaces_to_segment(self):
        res = mandarin_utils.pinyin_to_IPA("ba1 da2 tong1", use_spaces_to_segment=True)
        self.assertEqual(res, "pä˥˥ tä˧˥ tʰʊŋ˥˥")

    def test_special_case_ng(self):
        res = mandarin_utils.pinyin_to_IPA("ng5")
        self.assertEqual(res, "ŋ̍")

    def test_special_case_ri(self):
        res = mandarin_utils.pinyin_to_IPA("ri4")
        self.assertEqual(res, "ʐ̩˥˩")

    def test_syllable_with_v(self):
        res = mandarin_utils.pinyin_to_IPA("nv3")
        self.assertEqual(res, "ny˨˩˦")

        res = mandarin_utils.pinyin_to_IPA("qu4")
        self.assertEqual(res, "t͡ɕʰy˥˩")

    def test_voiceless_initial(self):
        res = mandarin_utils.pinyin_to_IPA("ge5")
        self.assertEqual(res, "g̊ə")

        res = mandarin_utils.pinyin_to_IPA("yi1 ge5")
        self.assertEqual(res, "i˥˥ g̊ə˨")

    def test_tone_three(self):
        res = mandarin_utils.pinyin_to_IPA("ke3")
        self.assertEqual(res, "kʰɤ˨˩˦")

        res = mandarin_utils.pinyin_to_IPA("ke3 yi3")
        self.assertEqual(res, "kʰɤ˨˩˦꜔꜒ i˨˩˦꜕꜖(꜓)")

    def test_tone_four(self):
        res = mandarin_utils.pinyin_to_IPA("xia4 qu4")
        self.assertEqual(res, "ɕjä˥˩꜒꜔ t͡ɕʰy˥˩")

        res = mandarin_utils.pinyin_to_IPA("xia4")
        self.assertEqual(res, "ɕjä˥˩")

    def test_other_tone(self):
        res = mandarin_utils.pinyin_to_IPA("ma1")
        self.assertEqual(res, "mä˥˥")

        res = mandarin_utils.pinyin_to_IPA("ma2")
        self.assertEqual(res, "mä˧˥")

        res = mandarin_utils.pinyin_to_IPA("ma5")
        self.assertEqual(res, "mä")

    def test_erhua(self):
        res = mandarin_utils.pinyin_to_IPA("huar1")
        self.assertEqual(res, "xu̯ɑɻ˥˥")

        res = mandarin_utils.pinyin_to_IPA("quanr1")
        self.assertEqual(res, "t͡ɕʰɥɑɻ˥˥")


class TestPinyinSegmentation(TestCase):
    def test_simple(self):
        _, res = mandarin_utils.segment_pinyin("guang3 dong1")
        self.assertEqual(res, ["guang3", "dong1"])

    def test_no_digits(self):
        _, res = mandarin_utils.segment_pinyin("guang dong")
        self.assertEqual(res, ["guang", "dong"])

    def test_no_spaces(self):
        _, res = mandarin_utils.segment_pinyin("guang3dong1")
        self.assertEqual(res, ["guang3", "dong1"])

    def test_no_digits_no_spaces(self):
        _, res = mandarin_utils.segment_pinyin("guangdong")
        self.assertEqual(res, ["guang", "dong"])

    def test_no_digits_apostrophe(self):
        _, res = mandarin_utils.segment_pinyin("xi'an")
        self.assertEqual(res, ["xi", "an"])

    def test_digits_apostrophe(self):
        _, res = mandarin_utils.segment_pinyin("xi1'an")
        self.assertEqual(res, ["xi1", "an"])

    def test_remove_special_characters(self):
        _, res = mandarin_utils.segment_pinyin("guang*dong!!")
        self.assertEqual(res, ["guang", "dong"])

    def test_keep_glob_characters(self):
        _, res = mandarin_utils.segment_pinyin(
            "guang* dong?", remove_glob_characters=False
        )
        self.assertEqual(res, ["guang", "* ", "dong", "?"])

    def test_keep_glob_characters_no_whitespace(self):
        _, res = mandarin_utils.segment_pinyin(
            "guang*dong?", remove_glob_characters=False
        )
        self.assertEqual(res, ["guang", "*", "dong", "?"])

    def test_keep_multiple_glob_characters(self):
        _, res = mandarin_utils.segment_pinyin(
            "guang?* dong", remove_glob_characters=False
        )
        self.assertEqual(res, ["guang", "?", "* ", "dong"])

    def test_keep_multiple_glob_characters_whitespace(self):
        _, res = mandarin_utils.segment_pinyin(
            "guang? * dong", remove_glob_characters=False
        )
        self.assertEqual(res, ["guang", "? ", "* ", "dong"])

    def test_keep_multiple_glob_characters_whitespace_surround(self):
        _, res = mandarin_utils.segment_pinyin(
            "guang ? * dong", remove_glob_characters=False
        )
        self.assertEqual(res, ["guang", " ? ", "* ", "dong"])

    def test_glob_characters_trim_whitespace(self):
        _, res = mandarin_utils.segment_pinyin(
            "guang  ?            *      dong", remove_glob_characters=False
        )
        self.assertEqual(res, ["guang", " ? ", "* ", "dong"])

    def test_keep_special_characters(self):
        _, res = mandarin_utils.segment_pinyin(
            "guang？ dong1", remove_special_characters=False
        )
        self.assertEqual(res, ["guang", "？", "dong1"])

    def test_remove_whitespace(self):
        _, res = mandarin_utils.segment_pinyin(
            "  guang                           dong      "
        )
        self.assertEqual(res, ["guang", "dong"])

    def test_lower(self):
        _, res = mandarin_utils.segment_pinyin("gUanGdOnG")
        self.assertEqual(res, ["guang", "dong"])

    def test_lower_with_digits(self):
        _, res = mandarin_utils.segment_pinyin("guAng3dONg1")
        self.assertEqual(res, ["guang3", "dong1"])

    def test_multiple_finals_vowels_only(self):
        _, res = mandarin_utils.segment_pinyin("ee")
        self.assertEqual(res, ["e", "e"])

    def test_multiple_finals(self):
        _, res = mandarin_utils.segment_pinyin("angang")
        self.assertEqual(res, ["ang", "ang"])

    def test_garbage(self):
        _, res = mandarin_utils.segment_pinyin("kljnxclkjvnl")
        self.assertEqual(res, ["kljnxclkjvnl"])
