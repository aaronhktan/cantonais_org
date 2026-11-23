from unittest import TestCase

from ..models import Example


class TestGetSourceLanguage(TestCase):
    def test_get_source_langauge(self):
        example = Example(
            source_language="yue",
            traditional = "臺山話",
            simplified = "台山话",
            jyutping = "toi4 saan1 waa2",
            pinyin = "tai2 shan1 hua4",
            translations=[])

        self.assertEqual(example.source_language, "yue")

class TestGetCharacters(TestCase):
    def test_get_traditional(self):
        example = Example(
            source_language="yue",
            traditional = "臺山話",
            simplified = "台山话",
            jyutping = "toi4 saan1 waa2",
            pinyin = "tai2 shan1 hua4",
            translations=[])

        self.assertEqual(example.traditional, "臺山話")

    def test_get_simplified(self):
        example = Example(
            source_language="yue",
            traditional = "臺山話",
            simplified = "台山话",
            jyutping = "toi4 saan1 waa2",
            pinyin = "tai2 shan1 hua4",
            translations=[])

        self.assertEqual(example.simplified, "台山话")


class TestGetPhonetic(TestCase):
    def test_get_cantonese(self):
        example = Example(
            source_language="yue",
            traditional = "臺山話",
            simplified = "台山话",
            jyutping = "toi4 saan1 waa2",
            pinyin = "tai2 shan1 hua4",
            translations=[])

        self.assertEqual(example.jyutping, "toi4 saan1 waa2")
        self.assertEqual(example._yale, "tòih sāan wá")
        self.assertEqual(example._cantonese_IPA, "tʰɔːi̯˨˩ säːn˥ wäː˧˥")

    def test_get_mandarin(self):
        example = Example(
            source_language="yue",
            traditional = "臺山話",
            simplified = "台山话",
            jyutping = "toi4 saan1 waa2",
            pinyin = "tai2 shan1 hua4",
            translations=[])

        self.assertEqual(example.pinyin, "tai2 shan1 hua4")
        self.assertEqual(example._pretty_pinyin, "tái shān huà")
        self.assertEqual(example._numbered_pinyin, "tai2 shan1 hua4")
        self.assertEqual(example._zhuyin, "ㄊㄞˊ ㄕㄢ ㄏㄨㄚˋ")
        self.assertEqual(example._mandarin_IPA, "tʰaɪ̯˧˥ ʂän˥˥ xu̯ä˥˩")
