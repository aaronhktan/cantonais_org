from unittest import TestCase

from ..utils import chinese_utils, default_settings


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

    def test_skip_same_characters(self):
        string = f"{chinese_utils.SAME_CHARACTER_STRING}{chinese_utils.SAME_CHARACTER_STRING}"
        tones = [4, 6]
        res = chinese_utils.apply_colours(
            string, tones, default_settings.DEFAULT_JYUTPING_TONES
        )
        self.assertEqual(
            res,
            f"{chinese_utils.SAME_CHARACTER_STRING}{chinese_utils.SAME_CHARACTER_STRING}",
        )

    def test_various_codepoints(self):
        string = "\u3400\U00020000\U0002a700\U0002b740\U0002b820\U0002ceb0\u0200"
        tones = [1, 2, 3, 4, 5, 6, 6]
        res = chinese_utils.apply_colours(
            string, tones, default_settings.DEFAULT_JYUTPING_TONES
        )
        self.assertEqual(
            res,
            (
                f'<span style="color: '
                f'{default_settings.DEFAULT_JYUTPING_TONES[1]}">\u3400</span>'
                f'<span style="color: '
                f'{default_settings.DEFAULT_JYUTPING_TONES[2]}">\U00020000</span>'
                f'<span style="color: '
                f'{default_settings.DEFAULT_JYUTPING_TONES[3]}">\U0002a700</span>'
                f'<span style="color: '
                f'{default_settings.DEFAULT_JYUTPING_TONES[4]}">\U0002b740</span>'
                f'<span style="color: '
                f'{default_settings.DEFAULT_JYUTPING_TONES[5]}">\U0002b820</span>'
                f'<span style="color: '
                f'{default_settings.DEFAULT_JYUTPING_TONES[6]}">\U0002ceb0</span>'
                f"\u0200"
            ),
        )

    def test_invalid_cantonese_tones(self):
        string = "唔係"
        tones = [4, 7]
        res = chinese_utils.apply_colours(
            string, tones, default_settings.DEFAULT_JYUTPING_TONES
        )
        self.assertEqual(
            res,
            (
                f'<span style="color: '
                f'{default_settings.DEFAULT_JYUTPING_TONES[4]}">唔</span>'
                f"係"
            ),
        )

    def test_invalid_mandarin_tones(self):
        string = "不是"
        tones = [7, 4]
        res = chinese_utils.apply_colours(
            string, tones, default_settings.DEFAULT_PINYIN_TONES
        )
        self.assertEqual(
            res,
            (
                f"不"
                f'<span style="color: '
                f'{default_settings.DEFAULT_PINYIN_TONES[4]}">是</span>'
            ),
        )

    def test_not_enough_tones(self):
        string = "唔係"
        tones = [4]
        res = chinese_utils.apply_colours(
            string, tones, default_settings.DEFAULT_JYUTPING_TONES
        )
        self.assertEqual(
            res,
            (
                f'<span style="color: '
                f'{default_settings.DEFAULT_JYUTPING_TONES[4]}">唔</span>'
                f"係"
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
