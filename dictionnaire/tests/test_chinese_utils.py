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

    def test_bad_numeric(self):
        string = "㒃"
        res = chinese_utils.extract_jyutping_tones(string)
        self.assertEqual(res, [])


class TestExtractPinyinTones(TestCase):
    def test_simple(self):
        string = "xiang1 gang3"
        res = chinese_utils.extract_pinyin_tones(string)
        self.assertEqual(res, [1, 3])

    def test_no_spaces(self):
        string = "xiang1gang3"
        res = chinese_utils.extract_pinyin_tones(string)
        self.assertEqual(res, [1, 3])

    def test_bad_numeric(self):
        string = "㒃"
        res = chinese_utils.extract_pinyin_tones(string)
        self.assertEqual(res, [])


class TestApplyColours(TestCase):
    def test_jyutping(self):
        string = "唔係"
        tones = [4, 6]
        res = chinese_utils.apply_colours(
            string, tones, default_settings.DEFAULT_JYUTPING_TONES
        )
        self.assertEqual(
            res,
            (
                f'<span style="color: '
                f'{default_settings.DEFAULT_JYUTPING_TONES[4]}">唔</span>'
                f'<span style="color: '
                f'{default_settings.DEFAULT_JYUTPING_TONES[6]}">係</span>'
            ),
        )

    def test_pinyin(self):
        string = "不是"
        tones = [2, 4]
        res = chinese_utils.apply_colours(
            string, tones, default_settings.DEFAULT_PINYIN_TONES
        )
        self.assertEqual(
            res,
            (
                f'<span style="color: '
                f'{default_settings.DEFAULT_PINYIN_TONES[2]}">不</span>'
                f'<span style="color: '
                f'{default_settings.DEFAULT_PINYIN_TONES[4]}">是</span>'
            ),
        )


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

    def test_reject_no_tone(self):
        res = chinese_utils.jyutping_to_yale("joeng")
        self.assertEqual(res, "joeng")

    def test_reject_single_letter(self):
        res = chinese_utils.jyutping_to_yale("a")
        self.assertEqual(res, "a")

    def test_reject_special_character(self):
        res = chinese_utils.jyutping_to_yale("-")
        self.assertEqual(res, "-")

    def test_no_spaces(self):
        res = chinese_utils.jyutping_to_yale("si1zi2saan1")
        self.assertEqual(res, "sī jí sāan")

    def test_spaces_to_segment(self):
        res = chinese_utils.jyutping_to_yale(
            "si1 zi2 saan1", use_spaces_to_segment=True
        )
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

    def test_tones(self):
        res = chinese_utils.jyutping_to_yale(
            "saam1 gau2 sei3 ling4 ng5 ji6 cat1 baat3 luk6"
        )
        self.assertEqual(res, "sāam gáu sei lìhng ńgh yih chāt baat luhk")

    def test_no_tone(self):
        res = chinese_utils.jyutping_to_yale("mit")
        self.assertEqual(res, "mit")


class TestJyutpingToIPA(TestCase):
    def test_simple(self):
        res = chinese_utils.jyutping_to_IPA("joeng4 sing4")
        self.assertEqual(res, "jœ̽ːŋ˨˩ sɪŋ˨˩")

    def test_reject_no_tone(self):
        res = chinese_utils.jyutping_to_IPA("joeng")
        self.assertEqual(res, "joeng")

    def test_reject_single_letter(self):
        res = chinese_utils.jyutping_to_IPA("a")
        self.assertEqual(res, "a")

    def test_reject_special_character(self):
        res = chinese_utils.jyutping_to_IPA("-")
        self.assertEqual(res, "-")

    def test_no_spaces(self):
        res = chinese_utils.jyutping_to_IPA("faa1sing4")
        self.assertEqual(res, "fäː˥ sɪŋ˨˩")

    def test_spaces_to_segment(self):
        res = chinese_utils.jyutping_to_IPA("joeng4 sing4", use_spaces_to_segment=True)
        self.assertEqual(res, "jœ̽ːŋ˨˩ sɪŋ˨˩")

    def test_preprocess_initial(self):
        res = chinese_utils.jyutping_to_IPA("zyu2 sung3")
        self.assertEqual(res, "t͡ʃyː˧˥ sʊŋ˧")

    def test_special_syllable(self):
        res = chinese_utils.jyutping_to_IPA("m4")
        self.assertEqual(res, "m̩˨˩")

    def test_checked_tone(self):
        res = chinese_utils.jyutping_to_IPA("sik6 si2 o1 faan6")
        self.assertEqual(res, "sɪk̚˨ siː˧˥ ɔː˥ fäːn˨")

    def test_special_final(self):
        res = chinese_utils.jyutping_to_IPA("uk1 kei2 jan4")
        self.assertEqual(res, "ʊk̚˥ kʰei̯˧˥ jɐn˨˩")

    def test_tones(self):
        res = chinese_utils.jyutping_to_IPA(
            "saam1 gau2 sei3 ling4 ng5 ji6 cat1 baat3 luk6"
        )
        self.assertEqual(res, "säːm˥ kɐu̯˧˥ sei̯˧ lɪŋ˨˩ ŋ̍˩˧ jiː˨ t͡sʰɐt̚˥ päːt̚˧ lʊk̚˨")

    def test_no_tone(self):
        res = chinese_utils.jyutping_to_yale("mok")
        self.assertEqual(res, "mok")


class TestPrettyPinyin(TestCase):
    def test_simple(self):
        res = chinese_utils.pretty_pinyin("shuai4 ge1")
        self.assertEqual(res, "shuài gē")

    def test_reject_no_tone(self):
        res = chinese_utils.pretty_pinyin("ba")
        self.assertEqual(res, "ba")

    def test_reject_single_letter(self):
        res = chinese_utils.pretty_pinyin("a")
        self.assertEqual(res, "a")

    def test_reject_special_character(self):
        res = chinese_utils.pretty_pinyin("-")
        self.assertEqual(res, "-")

    def test_secondary_vowel(self):
        res = chinese_utils.pretty_pinyin("hui4 tu2")
        self.assertEqual(res, "huì tú")

    def test_umlaut(self):
        res = chinese_utils.pretty_pinyin("nu:3 hai2")
        self.assertEqual(res, "nǚ hái")

    def test_tones(self):
        res = chinese_utils.pretty_pinyin("ma1 ma2 ma3 ma4")
        self.assertEqual(res, "mā má mǎ mà")

    def test_no_tone(self):
        res = chinese_utils.pretty_pinyin("nu")
        self.assertEqual(res, "nu")


class TestNumberedPinyin(TestCase):
    def test_simple(self):
        res = chinese_utils.numbered_pinyin("nu:3 hai2")
        self.assertEqual(res, "nü3 hai2")


class TestPinyinWithV(TestCase):
    def test_simple(self):
        res = chinese_utils.pinyin_with_v("nu:3 hai2")
        self.assertEqual(res, "nv3 hai2")


class TestPinyinToZhuyin(TestCase):
    def test_simple(self):
        res = chinese_utils.pinyin_to_zhuyin("ba1 da2 tong1")
        self.assertEqual(res, "ㄅㄚ ㄉㄚˊ ㄊㄨㄥ")

    def test_reject_no_tone(self):
        res = chinese_utils.pinyin_to_zhuyin("ba")
        self.assertEqual(res, "ba")

    def test_reject_single_letter(self):
        res = chinese_utils.pinyin_to_zhuyin("a")
        self.assertEqual(res, "a")

    def test_reject_special_character(self):
        res = chinese_utils.pinyin_to_zhuyin("-")
        self.assertEqual(res, "-")

    def test_no_spaces(self):
        res = chinese_utils.pinyin_to_zhuyin("ba1da2tong1")
        self.assertEqual(res, "ㄅㄚ ㄉㄚˊ ㄊㄨㄥ")

    def test_use_spaces_to_segment(self):
        res = chinese_utils.pinyin_to_zhuyin(
            "ba1 da2 tong1", use_spaces_to_segment=True
        )
        self.assertEqual(res, "ㄅㄚ ㄉㄚˊ ㄊㄨㄥ")

    def test_special_initials(self):
        res = chinese_utils.pinyin_to_zhuyin("qu4")
        self.assertEqual(res, "ㄑㄩˋ")

        res = chinese_utils.pinyin_to_zhuyin("chi1")
        self.assertEqual(res, "ㄔ")

        res = chinese_utils.pinyin_to_zhuyin("ri4")
        self.assertEqual(res, "ㄖˋ")

    def test_special_finals(self):
        res = chinese_utils.pinyin_to_zhuyin("hm5")
        self.assertEqual(res, "˙ㄏㄇ")

        res = chinese_utils.pinyin_to_zhuyin("hng5")
        self.assertEqual(res, "˙ㄏㄫ")

        res = chinese_utils.pinyin_to_zhuyin("er2")
        self.assertEqual(res, "ㄦˊ")

    def test_erhua(self):
        res = chinese_utils.pinyin_to_zhuyin("quanr1")
        self.assertEqual(res, "ㄑㄩㄢㄦ")

    def test_malformed(self):
        res = chinese_utils.pinyin_to_zhuyin("chzng2 quanr1")
        self.assertEqual(res, "ㄔzng2 ㄑㄩㄢㄦ")


class TestPinyinToIPA(TestCase):
    def test_simple(self):
        res = chinese_utils.pinyin_to_IPA("ba1 da2 tong1")
        self.assertEqual(res, "pä˥˥ tä˧˥ tʰʊŋ˥˥")

    def test_reject_no_tone(self):
        res = chinese_utils.pinyin_to_IPA("ba")
        self.assertEqual(res, "ba")

    def test_reject_single_letter(self):
        res = chinese_utils.pinyin_to_IPA("a")
        self.assertEqual(res, "a")

    def test_reject_special_character(self):
        res = chinese_utils.pinyin_to_IPA("-")
        self.assertEqual(res, "-")

    def test_no_spaces(self):
        res = chinese_utils.pinyin_to_IPA("ba1da2tong1")
        self.assertEqual(res, "pä˥˥ tä˧˥ tʰʊŋ˥˥")

    def test_use_spaces_to_segment(self):
        res = chinese_utils.pinyin_to_IPA("ba1 da2 tong1", use_spaces_to_segment=True)
        self.assertEqual(res, "pä˥˥ tä˧˥ tʰʊŋ˥˥")

    def test_special_case_ng(self):
        res = chinese_utils.pinyin_to_IPA("ng5")
        self.assertEqual(res, "ŋ̍")

    def test_special_case_ri(self):
        res = chinese_utils.pinyin_to_IPA("ri4")
        self.assertEqual(res, "ʐ̩˥˩")

    def test_syllable_with_v(self):
        res = chinese_utils.pinyin_to_IPA("nv3")
        self.assertEqual(res, "ny˨˩˦")

        res = chinese_utils.pinyin_to_IPA("qu4")
        self.assertEqual(res, "t͡ɕʰy˥˩")

    def test_voiceless_initial(self):
        res = chinese_utils.pinyin_to_IPA("ge5")
        self.assertEqual(res, "g̊ə")

        res = chinese_utils.pinyin_to_IPA("yi1 ge5")
        self.assertEqual(res, "i˥˥ g̊ə˨")

    def test_tone_three(self):
        res = chinese_utils.pinyin_to_IPA("ke3")
        self.assertEqual(res, "kʰɤ˨˩˦")

        res = chinese_utils.pinyin_to_IPA("ke3 yi3")
        self.assertEqual(res, "kʰɤ˨˩˦꜔꜒ i˨˩˦꜕꜖(꜓)")

    def test_tone_four(self):
        res = chinese_utils.pinyin_to_IPA("xia4 qu4")
        self.assertEqual(res, "ɕjä˥˩꜒꜔ t͡ɕʰy˥˩")

        res = chinese_utils.pinyin_to_IPA("xia4")
        self.assertEqual(res, "ɕjä˥˩")

    def test_other_tone(self):
        res = chinese_utils.pinyin_to_IPA("ma1")
        self.assertEqual(res, "mä˥˥")

        res = chinese_utils.pinyin_to_IPA("ma2")
        self.assertEqual(res, "mä˧˥")

        res = chinese_utils.pinyin_to_IPA("ma5")
        self.assertEqual(res, "mä")

    def test_erhua(self):
        res = chinese_utils.pinyin_to_IPA("huar1")
        self.assertEqual(res, "xu̯ɑɻ˥˥")

        res = chinese_utils.pinyin_to_IPA("quanr1")
        self.assertEqual(res, "t͡ɕʰɥɑɻ˥˥")


class TestJyutpingSegmentation(TestCase):
    def test_simple(self):
        _, res = chinese_utils.segment_jyutping("m4 goi1")
        self.assertEqual(res, ["m4", "goi1"])

    def test_no_digits(self):
        _, res = chinese_utils.segment_jyutping("m goi")
        self.assertEqual(res, ["m", "goi"])

    def test_no_spaces(self):
        _, res = chinese_utils.segment_jyutping("m4goi1")
        self.assertEqual(res, ["m4", "goi1"])

    def test_no_digits_no_spaces(self):
        _, res = chinese_utils.segment_jyutping("mgoi")
        self.assertEqual(res, ["m", "goi"])

    def test_no_digits_apostrophe(self):
        _, res = chinese_utils.segment_jyutping("m'aam")
        self.assertEqual(res, ["m", "aam"])

    def test_digits_apostrophe(self):
        _, res = chinese_utils.segment_jyutping("m4'aam")
        self.assertEqual(res, ["m4", "aam"])

    def test_remove_special_characters(self):
        _, res = chinese_utils.segment_jyutping("m*goi")
        self.assertEqual(res, ["m", "goi"])

    def test_keep_glob_characters(self):
        _, res = chinese_utils.segment_jyutping("m* goi", remove_glob_characters=False)
        self.assertEqual(res, ["m", "* ", "goi"])

    def test_keep_glob_characters_no_whitespace(self):
        _, res = chinese_utils.segment_jyutping("m*goi", remove_glob_characters=False)
        self.assertEqual(res, ["m", "*", "goi"])

    def test_keep_multiple_glob_characters(self):
        _, res = chinese_utils.segment_jyutping("m?* goi", remove_glob_characters=False)
        self.assertEqual(res, ["m", "?", "* ", "goi"])

    def test_keep_multiple_glob_characters_whitespace(self):
        _, res = chinese_utils.segment_jyutping(
            "m? * goi", remove_glob_characters=False
        )
        self.assertEqual(res, ["m", "? ", "* ", "goi"])

    def test_keep_multiple_glob_characters_whitespace_surround(self):
        _, res = chinese_utils.segment_jyutping(
            "m ? * goi", remove_glob_characters=False
        )
        self.assertEqual(res, ["m", " ? ", "* ", "goi"])

    def test_glob_characters_trim_whitespace(self):
        _, res = chinese_utils.segment_jyutping(
            "m  ?            *      goi", remove_glob_characters=False
        )
        self.assertEqual(res, ["m", " ? ", "* ", "goi"])

    def test_keep_special_characters(self):
        _, res = chinese_utils.segment_jyutping(
            "m？ goi", remove_special_characters=False
        )
        self.assertEqual(res, ["m", "？", "goi"])

    def test_remove_whitespace(self):
        _, res = chinese_utils.segment_jyutping(
            "  m                           goi      "
        )
        self.assertEqual(res, ["m", "goi"])

    def test_lower(self):
        _, res = chinese_utils.segment_jyutping("mGoI")
        self.assertEqual(res, ["m", "goi"])

    def test_lower_with_digits(self):
        _, res = chinese_utils.segment_jyutping("m4GoI1")
        self.assertEqual(res, ["m4", "goi1"])

    def test_multiple_finals_vowels_only(self):
        _, res = chinese_utils.segment_jyutping("aaaa")
        self.assertEqual(res, ["aa", "aa"])

    def test_multiple_finals_consonants_only(self):
        _, res = chinese_utils.segment_jyutping("ngng")
        self.assertEqual(res, ["ng", "ng"])

    def test_multiple_finals(self):
        _, res = chinese_utils.segment_jyutping("amam")
        self.assertEqual(res, ["am", "am"])

    def test_garbage(self):
        validity, res = chinese_utils.segment_jyutping("kljnxclkjvnl")
        self.assertEqual(validity, False)
        self.assertEqual(res, ["kljnxclkjvnl"])


class TestPinyinSegmentation(TestCase):
    def test_simple(self):
        _, res = chinese_utils.segment_pinyin("guang3 dong1")
        self.assertEqual(res, ["guang3", "dong1"])

    def test_no_digits(self):
        _, res = chinese_utils.segment_pinyin("guang dong")
        self.assertEqual(res, ["guang", "dong"])

    def test_no_spaces(self):
        _, res = chinese_utils.segment_pinyin("guang3dong1")
        self.assertEqual(res, ["guang3", "dong1"])

    def test_no_digits_no_spaces(self):
        _, res = chinese_utils.segment_pinyin("guangdong")
        self.assertEqual(res, ["guang", "dong"])

    def test_no_digits_apostrophe(self):
        _, res = chinese_utils.segment_pinyin("xi'an")
        self.assertEqual(res, ["xi", "an"])

    def test_digits_apostrophe(self):
        _, res = chinese_utils.segment_pinyin("xi1'an")
        self.assertEqual(res, ["xi1", "an"])

    def test_remove_special_characters(self):
        _, res = chinese_utils.segment_pinyin("guang*dong!!")
        self.assertEqual(res, ["guang", "dong"])

    def test_keep_glob_characters(self):
        _, res = chinese_utils.segment_pinyin(
            "guang* dong?", remove_glob_characters=False
        )
        self.assertEqual(res, ["guang", "* ", "dong", "?"])

    def test_keep_glob_characters_no_whitespace(self):
        _, res = chinese_utils.segment_pinyin(
            "guang*dong?", remove_glob_characters=False
        )
        self.assertEqual(res, ["guang", "*", "dong", "?"])

    def test_keep_multiple_glob_characters(self):
        _, res = chinese_utils.segment_pinyin(
            "guang?* dong", remove_glob_characters=False
        )
        self.assertEqual(res, ["guang", "?", "* ", "dong"])

    def test_keep_multiple_glob_characters_whitespace(self):
        _, res = chinese_utils.segment_pinyin(
            "guang? * dong", remove_glob_characters=False
        )
        self.assertEqual(res, ["guang", "? ", "* ", "dong"])

    def test_keep_multiple_glob_characters_whitespace_surround(self):
        _, res = chinese_utils.segment_pinyin(
            "guang ? * dong", remove_glob_characters=False
        )
        self.assertEqual(res, ["guang", " ? ", "* ", "dong"])

    def test_glob_characters_trim_whitespace(self):
        _, res = chinese_utils.segment_pinyin(
            "guang  ?            *      dong", remove_glob_characters=False
        )
        self.assertEqual(res, ["guang", " ? ", "* ", "dong"])

    def test_keep_special_characters(self):
        _, res = chinese_utils.segment_pinyin(
            "guang？ dong1", remove_special_characters=False
        )
        self.assertEqual(res, ["guang", "？", "dong1"])

    def test_remove_whitespace(self):
        _, res = chinese_utils.segment_pinyin(
            "  guang                           dong      "
        )
        self.assertEqual(res, ["guang", "dong"])

    def test_lower(self):
        _, res = chinese_utils.segment_pinyin("gUanGdOnG")
        self.assertEqual(res, ["guang", "dong"])

    def test_lower_with_digits(self):
        _, res = chinese_utils.segment_pinyin("guAng3dONg1")
        self.assertEqual(res, ["guang3", "dong1"])

    def test_multiple_finals_vowels_only(self):
        _, res = chinese_utils.segment_pinyin("ee")
        self.assertEqual(res, ["e", "e"])

    def test_multiple_finals(self):
        _, res = chinese_utils.segment_pinyin("angang")
        self.assertEqual(res, ["ang", "ang"])

    def test_garbage(self):
        _, res = chinese_utils.segment_pinyin("kljnxclkjvnl")
        self.assertEqual(res, ["kljnxclkjvnl"])
