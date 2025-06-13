from unittest import TestCase

from ..utils import cantonese_utils


class TestExtractJyutpingTones(TestCase):
    def test_simple(self):
        string = "zeng3 je5"
        res = cantonese_utils.extract_jyutping_tones(string)
        self.assertEqual(res, [3, 5])

    def test_no_spaces(self):
        string = "zeng3je5"
        res = cantonese_utils.extract_jyutping_tones(string)
        self.assertEqual(res, [3, 5])

    def test_bad_numeric(self):
        string = "㒃"
        res = cantonese_utils.extract_jyutping_tones(string)
        self.assertEqual(res, [])


class TestJyutpingToYale(TestCase):
    def test_simple(self):
        res = cantonese_utils.jyutping_to_yale("si1 zi2 saan1")
        self.assertEqual(res, "sī jí sāan")

    def test_reject_no_tone(self):
        res = cantonese_utils.jyutping_to_yale("joeng")
        self.assertEqual(res, "joeng")

    def test_reject_single_letter(self):
        res = cantonese_utils.jyutping_to_yale("a")
        self.assertEqual(res, "a")

    def test_reject_special_character(self):
        res = cantonese_utils.jyutping_to_yale("-")
        self.assertEqual(res, "-")

    def test_no_spaces(self):
        res = cantonese_utils.jyutping_to_yale("si1zi2saan1")
        self.assertEqual(res, "sī jí sāan")

    def test_spaces_to_segment(self):
        res = cantonese_utils.jyutping_to_yale(
            "si1 zi2 saan1", use_spaces_to_segment=True
        )
        self.assertEqual(res, "sī jí sāan")

    def test_special_final(self):
        res = cantonese_utils.jyutping_to_yale("goek3jyun5")
        self.assertEqual(res, "geuk yúhn")

    def test_light_tone(self):
        res = cantonese_utils.jyutping_to_yale("lok6 jyu5")
        self.assertEqual(res, "lohk yúh")

    def test_special_syllable(self):
        res = cantonese_utils.jyutping_to_yale("m4 hai6")
        self.assertEqual(res, "m̀h haih")

    def test_tones(self):
        res = cantonese_utils.jyutping_to_yale(
            "saam1 gau2 sei3 ling4 ng5 ji6 cat1 baat3 luk6"
        )
        self.assertEqual(res, "sāam gáu sei lìhng ńgh yih chāt baat luhk")

    def test_no_tone(self):
        res = cantonese_utils.jyutping_to_yale("mit")
        self.assertEqual(res, "mit")


class TestJyutpingToIPA(TestCase):
    def test_simple(self):
        res = cantonese_utils.jyutping_to_IPA("joeng4 sing4")
        self.assertEqual(res, "jœ̽ːŋ˨˩ sɪŋ˨˩")

    def test_reject_no_tone(self):
        res = cantonese_utils.jyutping_to_IPA("joeng")
        self.assertEqual(res, "joeng")

    def test_reject_single_letter(self):
        res = cantonese_utils.jyutping_to_IPA("a")
        self.assertEqual(res, "a")

    def test_reject_special_character(self):
        res = cantonese_utils.jyutping_to_IPA("-")
        self.assertEqual(res, "-")

    def test_no_spaces(self):
        res = cantonese_utils.jyutping_to_IPA("faa1sing4")
        self.assertEqual(res, "fäː˥ sɪŋ˨˩")

    def test_spaces_to_segment(self):
        res = cantonese_utils.jyutping_to_IPA("joeng4 sing4", use_spaces_to_segment=True)
        self.assertEqual(res, "jœ̽ːŋ˨˩ sɪŋ˨˩")

    def test_preprocess_initial(self):
        res = cantonese_utils.jyutping_to_IPA("zyu2 sung3")
        self.assertEqual(res, "t͡ʃyː˧˥ sʊŋ˧")

    def test_special_syllable(self):
        res = cantonese_utils.jyutping_to_IPA("m4")
        self.assertEqual(res, "m̩˨˩")

    def test_checked_tone(self):
        res = cantonese_utils.jyutping_to_IPA("sik6 si2 o1 faan6")
        self.assertEqual(res, "sɪk̚˨ siː˧˥ ɔː˥ fäːn˨")

    def test_special_final(self):
        res = cantonese_utils.jyutping_to_IPA("uk1 kei2 jan4")
        self.assertEqual(res, "ʊk̚˥ kʰei̯˧˥ jɐn˨˩")

    def test_tones(self):
        res = cantonese_utils.jyutping_to_IPA(
            "saam1 gau2 sei3 ling4 ng5 ji6 cat1 baat3 luk6"
        )
        self.assertEqual(res, "säːm˥ kɐu̯˧˥ sei̯˧ lɪŋ˨˩ ŋ̍˩˧ jiː˨ t͡sʰɐt̚˥ päːt̚˧ lʊk̚˨")

    def test_no_tone(self):
        res = cantonese_utils.jyutping_to_yale("mok")
        self.assertEqual(res, "mok")


class TestJyutpingSegmentation(TestCase):
    def test_simple(self):
        _, res = cantonese_utils.segment_jyutping("m4 goi1")
        self.assertEqual(res, ["m4", "goi1"])

    def test_no_digits(self):
        _, res = cantonese_utils.segment_jyutping("m goi")
        self.assertEqual(res, ["m", "goi"])

    def test_no_spaces(self):
        _, res = cantonese_utils.segment_jyutping("m4goi1")
        self.assertEqual(res, ["m4", "goi1"])

    def test_no_digits_no_spaces(self):
        _, res = cantonese_utils.segment_jyutping("mgoi")
        self.assertEqual(res, ["m", "goi"])

    def test_no_digits_apostrophe(self):
        _, res = cantonese_utils.segment_jyutping("m'aam")
        self.assertEqual(res, ["m", "aam"])

    def test_digits_apostrophe(self):
        _, res = cantonese_utils.segment_jyutping("m4'aam")
        self.assertEqual(res, ["m4", "aam"])

    def test_remove_special_characters(self):
        _, res = cantonese_utils.segment_jyutping("m*goi")
        self.assertEqual(res, ["m", "goi"])

    def test_keep_glob_characters(self):
        _, res = cantonese_utils.segment_jyutping("m* goi", remove_glob_characters=False)
        self.assertEqual(res, ["m", "* ", "goi"])

    def test_keep_glob_characters_no_whitespace(self):
        _, res = cantonese_utils.segment_jyutping("m*goi", remove_glob_characters=False)
        self.assertEqual(res, ["m", "*", "goi"])

    def test_keep_multiple_glob_characters(self):
        _, res = cantonese_utils.segment_jyutping("m?* goi", remove_glob_characters=False)
        self.assertEqual(res, ["m", "?", "* ", "goi"])

    def test_keep_multiple_glob_characters_whitespace(self):
        _, res = cantonese_utils.segment_jyutping(
            "m? * goi", remove_glob_characters=False
        )
        self.assertEqual(res, ["m", "? ", "* ", "goi"])

    def test_keep_multiple_glob_characters_whitespace_surround(self):
        _, res = cantonese_utils.segment_jyutping(
            "m ? * goi", remove_glob_characters=False
        )
        self.assertEqual(res, ["m", " ? ", "* ", "goi"])

    def test_glob_characters_trim_whitespace(self):
        _, res = cantonese_utils.segment_jyutping(
            "m  ?            *      goi", remove_glob_characters=False
        )
        self.assertEqual(res, ["m", " ? ", "* ", "goi"])

    def test_keep_special_characters(self):
        _, res = cantonese_utils.segment_jyutping(
            "m？ goi", remove_special_characters=False
        )
        self.assertEqual(res, ["m", "？", "goi"])

    def test_remove_whitespace(self):
        _, res = cantonese_utils.segment_jyutping(
            "  m                           goi      "
        )
        self.assertEqual(res, ["m", "goi"])

    def test_lower(self):
        _, res = cantonese_utils.segment_jyutping("mGoI")
        self.assertEqual(res, ["m", "goi"])

    def test_lower_with_digits(self):
        _, res = cantonese_utils.segment_jyutping("m4GoI1")
        self.assertEqual(res, ["m4", "goi1"])

    def test_multiple_finals_vowels_only(self):
        _, res = cantonese_utils.segment_jyutping("aaaa")
        self.assertEqual(res, ["aa", "aa"])

    def test_multiple_finals_consonants_only(self):
        _, res = cantonese_utils.segment_jyutping("ngng")
        self.assertEqual(res, ["ng", "ng"])

    def test_multiple_finals(self):
        _, res = cantonese_utils.segment_jyutping("amam")
        self.assertEqual(res, ["am", "am"])

    def test_garbage(self):
        validity, res = cantonese_utils.segment_jyutping("kljnxclkjvnl")
        self.assertEqual(validity, False)
        self.assertEqual(res, ["kljnxclkjvnl"])
