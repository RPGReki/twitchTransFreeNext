from dotenv import load_dotenv
import os

load_dotenv()

Twitch_Channel          = 'RPGReki'
Trans_Username          = 'AiteUsagi'
Bot_Prefix              = '?'
Trans_OAUTH             = os.environ['TWITTER_OAUTH']

Trans_TextColor         = 'Red'

lang_TransToHome        = 'en'
lang_HomeToOther        = 'en'
lang_Fallback           = 'en'


Show_ByName             = True
Show_ByLang             = True

Ignore_Lang             = []
Ignore_Users            = []
Ignore_Line             = ['http']
Delete_Words            = []

# Any emvironment, set it to `True`, then text will be read by TTS voice!
# TTS_In:User Input Text, TTS_Out:Bot Output Text
TTS_In                  = True
TTS_Out                 = True
TTS_Kind                = "gTTS" # You can choice "CeVIO" if you want to use CeVIO as TTS.
TTS_TextMaxLength       = 500
# CeVIO_Cast            = "さとうささら" # When you are using CeVIO, you must set voice cast name.

TTS_Substitutions       = {
    "en": [
        ['\\b([0-9])[pP]\\b', '\\1 dots'],
        ['\\b([0-9])[sS]\\b', '\\1 bamboo'],
        ['\\b([0-9])[mM]\\b', '\\1 characters'],
        ['\\b1[zZ]\\b', 'east'],
        ['\\b2[zZ]\\b', 'south'],
        ['\\b3[zZ]\\b', 'west'],
        ['\\b4[zZ]\\b', 'north'],
        ['\\b5[zZ]\\b', 'white'],
        ['\\b6[zZ]\\b', 'green'],
        ['\\b7[zZ]\\b', 'red'],
        ['\\brpgrek[A-Z][a-zA-Z0-9]*\\b', ''],
        ['\\Da\\b', 'The']
    ]
}

ReadOnlyTheseLang       = ['en']

# Select the translate engine ('deepl' or 'google')
Translator              = 'deepl' #'google'
GAS_URL                 = ''
GoogleTranslate_suffix  = 'de'

Debug                   = True
