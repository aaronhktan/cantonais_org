from unittest import TestCase

from ..models import Definition, DefinitionsSet


class TestDefinitionsSet(TestCase):
    def test_definitions_snippet(self):
        definition = Definition(
            definition_content="Qingyuan, prefecture-level city in Guangdong",
            label="",
            examples=[])
        definitionsSet = DefinitionsSet(
            source="CC-CANTO",
            definitions=[definition])

        self.assertEqual(definitionsSet._definitions_snippet, "Qingyuan, prefecture-level city in Guangdong")

    def test_definitions_snippet_empty_definition_content(self):
        definition = Definition(
            definition_content="",
            label="",
            examples=[])
        definitionsSet = DefinitionsSet(
            source="CC-CANTO",
            definitions=[definition])

        self.assertEqual(definitionsSet._definitions_snippet, "")

    def test_definitions_snippet_empty_definitions(self):
        definitionsSet = DefinitionsSet(
            source="CC-CANTO",
            definitions=[])

        self.assertEqual(definitionsSet._definitions_snippet, "")

    def test_source_simple(self):
        definitionsSet = DefinitionsSet(
            source="CC-CANTO",
            definitions=[])

        self.assertEqual(definitionsSet.source, "CC-CANTO")
