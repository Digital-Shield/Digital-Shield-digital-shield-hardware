import sys
from storage import device

from trezor import log, utils
class Language:
    def __init__(self, code, name):
        self.code = code
        self.name = name

languages = [
    # Language('zh_cn', '简体中文'),
    Language('zh_hk', '繁體中文'),
    Language('en', 'English'),
    Language('th','한국어'),
    Language('ja','日語'),
    Language("al","بالعربية"),
    Language('yn','Tiếng Việt'),
    Language('de','Deutsch'),
]



def change_language(lang: str | Language | None = None):
    if not lang:
        lang = device.get_language()
        log.debug(__name__, f"device stored language: {lang}")
    elif isinstance(lang, Language):
        lang = lang.code
        log.debug(__name__, f"selected language: {lang}")
    elif isinstance(lang, str):
        log.debug(__name__, f"user language: {lang}")
        lang = lang or device.get_language()

    log.debug(__name__, f"changing language: {lang}")

    if lang == 'en':
        from . import en as lang_module
    elif lang == 'zh_cn':
        from . import zh_cn as lang_module
    elif lang == 'zh_hk':
        from . import zh_hk as lang_module
    elif lang == 'th':
        from . import th as lang_module
    elif lang == 'ja':
        from . import ja as lang_module
    elif lang == 'al':
        from . import al as lang_module
    elif lang == 'yn':
        from . import yn as lang_module
    elif lang == 'de':
        from . import de as lang_module
    else:
        raise ValueError(f"Unsupported language: {lang}")
    global using
    using = utils.first(languages, lambda l: l.code == lang) or languages[0]
    for attr in dir(lang_module):
        if attr.startswith('_'):
            continue
        setattr(sys.modules[__name__], attr, getattr(lang_module, attr))

    del lang_module

# default language,
_default = 'zh_hk' if not device.is_initialized() else None
using :Language | None = None
change_language(_default)
# now using must not be None

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from en import *
