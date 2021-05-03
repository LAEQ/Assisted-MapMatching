import os
import unittest

from services.translator import Translator


class TestTranslator(unittest.TestCase):
    def setUp(self) -> None:
        self.service = Translator()
        pass

    def test_default_locale(self):
        default = self.service.get_locale()
        self.assertEqual("en", default)

    def test_locale_none(self):
        default = self.service.get_locale()
        self.assertEqual("en", default)

    def test_local_path(self):
        local_path = self.service.locale_path()
        self.assertTrue(os.path.exists(local_path))

    def test_translation(self):
        result = self.service.translate("@default")
        print(result)