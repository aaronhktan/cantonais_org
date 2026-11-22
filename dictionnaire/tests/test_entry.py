from unittest import TestCase

from ..models import Entry
from ..utils import default_settings, chinese_utils


class TestGetCharacters(TestCase):
    def test_colour_cantonese(self):
        entry = Entry(
            traditional="清遠",
            simplified="清远",
            jyutping="cing1 jyun5",
            pinyin="qing1 yuan3",
            definitions_sets=[],
        )

        self.assertEqual(
            entry._coloured_traditional,
            f'<span style="color: {default_settings.DEFAULT_JYUTPING_TONES[1]}">清</span>'
            f'<span style="color: {default_settings.DEFAULT_JYUTPING_TONES[5]}">遠</span>',
        )

        self.assertEqual(
            entry._coloured_simplified,
            f'<span style="color: {default_settings.DEFAULT_JYUTPING_TONES[1]}">清</span>'
            f'<span style="color: {default_settings.DEFAULT_JYUTPING_TONES[5]}">远</span>',
        )

        self.assertEqual(
            entry._traditional_difference, f"{chinese_utils.SAME_CHARACTER_STRING}遠"
        )

        self.assertEqual(
            entry._simplified_difference, f"{chinese_utils.SAME_CHARACTER_STRING}远"
        )

        self.assertEqual(
            entry._coloured_traditional_difference,
            f"{chinese_utils.SAME_CHARACTER_STRING}"
            f'<span style="color: {default_settings.DEFAULT_JYUTPING_TONES[5]}">遠</span>',
        )

        self.assertEqual(
            entry._coloured_simplified_difference,
            f"{chinese_utils.SAME_CHARACTER_STRING}"
            f'<span style="color: {default_settings.DEFAULT_JYUTPING_TONES[5]}">远</span>',
        )


class TestGetPhonetic(TestCase):
    def test_cantonese(self):
        entry = Entry(
            traditional="清遠",
            simplified="清远",
            jyutping="cing1 jyun5",
            pinyin="qing1 yuan3",
            definitions_sets=[],
        )

        self.assertEqual(entry.jyutping, "cing1 jyun5")
        self.assertEqual(entry._yale, "chīng yúhn")
        self.assertEqual(entry._cantonese_IPA, "t͡sʰɪŋ˥ jyːn˩˧")

    def test_mandarin(self):
        entry = Entry(
            traditional="清遠",
            simplified="清远",
            jyutping="cing1 jyun5",
            pinyin="qing1 yuan3",
            definitions_sets=[],
        )

        self.assertEqual(entry.pinyin, "qing1 yuan3")
        self.assertEqual(entry._pretty_pinyin, "qīng yuǎn")
        self.assertEqual(entry._numbered_pinyin, "qing1 yuan3")
        self.assertEqual(entry._zhuyin, "ㄑㄧㄥ ㄩㄢˇ")
        self.assertEqual(entry._mandarin_IPA, "t͡ɕʰiŋ˥˥ ɥɛn˨˩˦꜕꜖(꜓)")
