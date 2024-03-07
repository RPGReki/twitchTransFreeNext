from dotenv import load_dotenv
import os

load_dotenv()

Twitch_Channels         = ['rpgreki']
Twitch_Channel          = 'rpgreki'
Trans_Username          = 'flufflekeeper'
Bot_Prefix              = '!'
Trans_OAUTH             = os.environ['TWITTER_OAUTH']

Trans_TextColor         = 'Red'

lang_TransToHome        = 'en'
lang_HomeToOther        = 'de'
lang_Fallback           = 'en'


Show_ByName             = True
Show_ByLang             = True

Ignore_Lang             = []
Ignore_Users            = ['WarpWorldBot']
Ignore_Line             = ['-> The stream', '-> Current Stream', 'Currently playing', '(╯°□°）╯', 'Da bunnies are invading!', 'via reward)', '(auto timer)']
Delete_Words            = []

# Any emvironment, set it to `True`, then text will be read by TTS voice!
# TTS_In:User Input Text, TTS_Out:Bot Output Text
TTS_In                  = True
TTS_Out                 = True
TTS_Kind                = "gTTS" # You can choice "CeVIO" if you want to use CeVIO as TTS.
TTS_TextMaxLength       = 500
# CeVIO_Cast            = "さとうささら" # When you are using CeVIO, you must set voice cast name.


# Substitutions will be made before emote detection

TTS_Substitutions       = {
    "en": [
        ['<se.[0-9]*>', ''],
        ['https://\\S*', ''],
        ['(Link: |via |at: |)https://\\S*', ''],
        ['RPGReki', 'RPG Reki'],
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
        ['\\bDa\\b', 'The'],
        ['!([0-9a-zA-Z]\S*)', 'exclamation mark \\1.'],
        ['\\bGLA\\b','gladiator'], ['\\bPLD\\b','paladin'],
        ['\\bMRD\\b','marauder'],  ['\\bWAR\\b','warrior'],
        ['\\bDRK\\b','dark knight'],
        ['\\bGNB\\b','gun breaker'],
        ['\\bCNJ\\b','conjurer'],  ['\\bWHM\\b','white mage'],
        ['\\bSCH\\b','scholar'],
        ['\\bAST\\b','astrologian'],
        ['\\bSAG\\b','sage'],
        ['\\bPGL\\b','pugilist'], ['\\bMNK\\b','monk'],
        ['\\bSAM\\b','samurai'],
        ['\\bLNC\\b','lancer'], ['\\bDRG\\b','dragoon'],
        ['\\bROG\\b','rogue'], ['\\bNIN\\b','ninja'],
        ['\\bARC\\b','archer'],['\\bBRD\\b','bard'],
        ['\\bMCH\\b','machinist'],
        ['\\bDNC\\b','dancer'],
        ['\\bTHM\\b','pugilist'], ['\\bBLM\\b','black mage'],
        ['\\bACN\\b','arcanist'], ['\\bSMN\\b','summoner'],
        ['\\bRDM\\b','red mage'],
        ['\\bBLU\\b','blue mage']
    ],
    "de": [
       ['https://\\S*', ''],
       ['RPGReki', 'RPG Reki'],
    ],
    "ja": [
        ['https://\\S*', ''],
        ['RPGReki', 'RPG Reki'],
    ],
    "un": [
        ['https://\\S*', ''],
        ['RPGReki', 'RPG Reki'],
    ],
    "vi": [
        ['https://\\S*', ''],
        ['RPGReki', 'RPG Reki'],
    ]
}

ReadOnlyTheseLang       = ["en", "ja"]

# Select the translate engine ('deepl' or 'google')
Translator              = 'deepl' #'google'
GAS_URL                 = ''
GoogleTranslate_suffix  = 'de'
GoogleTTS_suffix        = 'de'

Debug                   = False

Quotes = [
    "“Oh mein Gott! It's Limit Cut!!” — RPGReki, October 2023",
    "“I'm a rather wet bunny… or should I say moist?” — RPGReki, September 2023",
]
