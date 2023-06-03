######################################################
# PLEASE CHANGE FOLLOWING CONFIGS ####################
Twitch_Channel          = 'RPGReki'

Trans_Username          = 'CompanionBunny'
Trans_OAUTH             = ''

#######################################################
# OPTIONAL CONFIGS ####################################
Trans_TextColor         = 'Red'
# Blue, Coral, DodgerBlue, SpringGreen, YellowGreen, Green, OrangeRed, Red, GoldenRod, HotPink, CadetBlue, SeaGreen, Chocolate, BlueViolet, and Firebrick

lang_TransToHome        = 'en'
lang_HomeToOther        = 'de'

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

# if you make TTS for only few lang, please add langID in the list
# for example, ['ja'] means Japanese only, ['ko','en'] means Korean and English are TTS!
ReadOnlyTheseLang       = ['en', '']

# Select the translate engine ('deepl' or 'google')
Translator              = 'deepl' #'google'

# Use Google Apps Script for tlanslating
# e.g.) GAS_URL         = 'https://script.google.com/macros/s/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/exec'
GAS_URL                 = ''

# Enter the suffix of the Google Translate URL you normally use.
# Example: translate.google.co.jp -> 'co.jp'
#          translate.google.com   -> 'com'
GoogleTranslate_suffix  = 'de'

# If you meet any bugs, You can check some error message using Debug mode (Debug = True)
Debug                   = True

