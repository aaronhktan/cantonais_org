from dataclasses import dataclass

# Python doesn't really have a good way to hide fields,
# so I'm just gonna use a single underscore prefix to
# denote a read-only member of a class


@dataclass
class Entry:
    traditional: str
    _traditionalDifference: str
    simplified: str
    _simplifiedDifference: str

    jyutping: str
    _yale: str
    _cantoneseIPA: str

    pinyin: str
    _prettypinyin: str
    _numberedPinyin: str
    _zhuyin: str
    _mandarinIPA: str

    definitionsSets: list = None

    def __post_init__(self):


@dataclass
class Definition:
    definitionContent: str
    label: str
    sentences: list = None


@dataclass
class DefinitionsSet:
    definitions: list = None
    source: str
    _sourceShortString: str
    _definitionsSnippet: str


@dataclass
class SourceSentence:
    sourceLanguage: str
    simplified: str
    traditional: str

    jyutping: str
    _yale: str
    _cantoneseIPA: str

    pinyin: str
    _prettypinyin: str
    _numberedPinyin: str
    _zhuyin: str
    _mandarinIPA: str

    translations: list = None


@dataclass
class Translation:
    translation: str
    language: str


@dataclass
class TranslationSet:
    translations: list = None
    source: str
    _sourceShortString: str
    _sentenceSnippet: str
