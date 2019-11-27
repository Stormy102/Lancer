import gettext

translation = gettext.translation('lancer', localedir='locale', languages=['en'])
translation.install()
_ = translation.gettext


def update_translation(language: str) -> None:
    global translation
    translation = gettext.translation('lancer', localedir='locale', languages=[language])


print((_("Lancer.Startup")).format(VERSION="0.0.3 Alpha", OS="Windows", OS_VERSION="10"))
