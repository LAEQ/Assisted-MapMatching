import os
from qgis.PyQt.QtCore import QCoreApplication, QTranslator, QSettings


class Translator:
    """
    Translator service
    """
    def __init__(self):
        self.current_dir = os.path.dirname(__file__)
        self.default_locale = "en"
        self.supported_locales = ["en", "fr", "es"]
        translator = QTranslator()
        translator.load(self.locale_path())
        QCoreApplication.installTranslator(translator)

    def supported_locale(self, locale):
        if locale in self.supported_locales:
            return locale

        return self.default_locale

    def get_locale(self):
        locale = QSettings().value('locale/userLocale', defaultValue=self.default_locale)

        return self.supported_locale(locale)

    def locale_path(self):
        return os.path.join(self.current_dir,
                            '..',
                            'i18n',
                            'messages_{}.qm'.format(self.get_locale()))

    def translate(self, key):
        return QCoreApplication.translate('MapMatching', key)
