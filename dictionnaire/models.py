from dataclasses import dataclass

from .utils import chinese_utils, default_settings

# Python doesn't really have a good way to hide fields,
# so I'm just gonna use a single underscore prefix to
# denote a read-only member of a class


@dataclass
class Translation:
    translation: str
    language: str


@dataclass
class TranslationSet:
    source: str
    _sourceShortString: str
    _sentenceSnippet: str

    translations: list[Translation] | None = None


@dataclass
class SourceSentence:
    sourceLanguage: str
    simplified: str
    traditional: str

    jyutping: str
    pinyin: str

    _yale: str | None = None
    _cantonese_IPA: str | None = None

    _pretty_pinyin: str | None = None
    _numbered_pinyin: str | None = None
    _zhuyin: str | None = None
    _mandarin_IPA: str | None = None

    translations: list[TranslationSet] | None = None

    def __post_init__(self):
        self._yale = chinese_utils.jyutping_to_yale(self.jyutping)
        self._cantonese_IPA = chinese_utils.jyutping_to_IPA(self.jyutping)

        self._pretty_pinyin = chinese_utils.pretty_pinyin(self.pinyin)
        self._numbered_pinyin = chinese_utils.numbered_pinyin(self.pinyin)
        self._zhuyin = chinese_utils.pinyin_to_zhuyin(self.pinyin)
        self._mandarin_IPA = chinese_utils.pinyin_to_IPA(self.pinyin)


@dataclass
class Definition:
    definition_content: str
    label: str
    sentences: list[SourceSentence] | None = None


@dataclass
class DefinitionsSet:
    source: str
    definitions: list[Definition] | None = None
    _definitions_snippet: str | None = None

    def __post_init__(self):
        # Generate the definitions snippet
        self._definitions_snippet = "; ".join(
            definition.definition_content for definition in self.definitions)


@dataclass
class Entry:
    traditional: str
    simplified: str

    jyutping: str
    pinyin: str

    _coloured_traditional: str | None = None
    _coloured_simplified: str | None = None

    _traditional_difference: str | None = None
    _coloured_traditional_difference: str | None = None
    _simplified_difference: str | None = None
    _coloured_simplified_difference: str | None = None

    _yale: str | None = None
    _cantonese_IPA: str | None = None

    _pretty_pinyin: str | None = None
    _numbered_pinyin: str | None = None
    _zhuyin: str | None = None
    _mandarin_IPA: str | None = None

    definitions_sets: list[DefinitionsSet] | None = None

    def __post_init__(self):
        # Generate all the read-only fields
        self._coloured_traditional = chinese_utils.apply_colours(
            self.traditional, chinese_utils.extract_jyutping_tones(
                self.jyutping),
            default_settings.DEFAULT_JYUTPING_TONES
        )
        self._coloured_simplified = chinese_utils.apply_colours(
            self.traditional, chinese_utils.extract_jyutping_tones(
                self.jyutping),
            default_settings.DEFAULT_JYUTPING_TONES
        )

        self._traditional_difference = chinese_utils.compare_strings(
            self.simplified, self.traditional)
        self._coloured_traditional_difference = chinese_utils.apply_colours(
            self._traditional_difference, chinese_utils.extract_jyutping_tones(
                self.jyutping),
            default_settings.DEFAULT_JYUTPING_TONES
        )
        self._simplified_difference = chinese_utils.compare_strings(
            self.traditional, self.simplified)
        self._coloured_simplified_difference = chinese_utils.apply_colours(
            self._simplified_difference, chinese_utils.extract_jyutping_tones(
                self.jyutping),
            default_settings.DEFAULT_JYUTPING_TONES
        )

        self._yale = chinese_utils.jyutping_to_yale(self.jyutping)
        self._cantonese_IPA = chinese_utils.jyutping_to_IPA(self.jyutping)

        self._pretty_pinyin = chinese_utils.pretty_pinyin(self.pinyin)
        self._numbered_pinyin = chinese_utils.numbered_pinyin(self.pinyin)
        self._zhuyin = chinese_utils.pinyin_to_zhuyin(self.pinyin)
        self._mandarin_IPA = chinese_utils.pinyin_to_IPA(self.pinyin)
