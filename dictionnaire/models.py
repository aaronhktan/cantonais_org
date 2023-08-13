from dataclasses import dataclass

# Python doesn't really have a good way to hide fields,
# so I'm just gonna use a single underscore prefix to
# denote a read-only member of a class


@dataclass
class Entry:
    traditional: str
    simplified: str

    jyutping: str
    pinyin: str

    _traditionalDifference: str = None
    _simplifiedDifference: str = None

    _yale: str = None
    _cantoneseIPA: str = None

    _prettypinyin: str = None
    _numberedPinyin: str = None
    _zhuyin: str = None
    _mandarinIPA: str = None

    definitionsSets: list = None

    def __post_init__(self):
        # TODO: Generate members with _
        pass


@dataclass
class Definition:
    definitionContent: str
    label: str
    sentences: list = None


@dataclass
class DefinitionsSet:
    source: str
    _sourceShortString: str
    _definitionsSnippet: str

    definitions: list = None

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
    source: str
    _sourceShortString: str
    _sentenceSnippet: str

    translations: list = None
