#!/usr/bin/env python
# -*- coding: utf-8 -*-

from async_google_trans_new import AsyncTranslator, constant
from http.client import HTTPSConnection as hc
from twitchio.ext import commands
from emoji import distinct_emoji_list
import json, os, shutil, re, asyncio, deepl, sys, signal, tts, sound, re, d20, uwuify, random, queue
import database_controller as db # en:Translation Database

version = '2.5.1-rpgreki'

#####################################
# 初期設定 ###########################

# configure for Google TTS & play
TMP_DIR = f'{os.path.dirname(sys.argv[0])}/tmp/'

# translate.googleのサフィックスリスト
URL_SUFFIX_LIST = [re.search('translate.google.(.*)', url.strip()).group(1) for url in constant.DEFAULT_SERVICE_URLS]

TargetLangs = ["af", "sq", "am", "ar", "hy", "az", "eu", "be", "bn", "bs", "bg", "ca", "ceb", "ny", "zh-CN", "zh-TW", "co",
                "hr", "cs", "da", "nl", "en", "eo", "et", "tl", "fi", "fr", "fy", "gl", "ka", "de", "el", "gu", "ht", "ha",
                "haw", "iw", "hi", "hmn", "hu", "is", "ig", "id", "ga", "it", "ja", "jw", "kn", "kk", "km", "ko", "ku", "ky",
                "lo", "la", "lv", "lt", "lb", "mk", "mg", "ms", "ml", "mt", "mi", "mr", "mn", "my", "ne", "no", "ps", "fa",
                "pl", "pt", "ma", "ro", "ru", "sm", "gd", "sr", "st", "sn", "sd", "si", "sk", "sl", "so", "es", "su", "sw",
                "sv", "tg", "ta", "te", "th", "tr", "uk", "ur", "uz", "vi", "cy", "xh", "yi", "yo", "zu"]

deepl_lang_dict = {'de':'DE', 'en':'EN', 'fr':'FR', 'es':'ES', 'pt':'PT', 'it':'IT', 'nl':'NL', 'pl':'PL', 'ru':'RU', 'ja':'JA', 'zh-CN':'ZH'}

ptts_text = ""

##########################################
# load config text #######################
import importlib

# For [directly run from Python script at Windows, MacOS] -----------------------
try:
    sys.path.append(os.path.dirname(sys.argv[0]))
    config = importlib.import_module('config')
except Exception as e:
    print(e)
    print('Please make [config.py] and put it with twitchTransFN')
    input() # stop for error!!

###################################
# fix some config errors ##########

# convert depreated gTTS_In, gTTS_Out => TTS_in, TTS_Out ------
if hasattr(config, 'gTTS_In') and not hasattr(config, 'TTS_In'):
    print('[warn] gTTS_In is already deprecated, please use TTS_In instead.')
    config.TTS_In = config.gTTS_In

if hasattr(config, 'gTTS_Out') and not hasattr(config, 'TTS_Out'):
    print('[warn] gTTS_Out is already deprecated, please use TTS_Out instead.')
    config.TTS_Out = config.gTTS_Out


# 無視言語リストの準備 ################
Ignore_Lang = [x.strip() for x in config.Ignore_Lang]

# 無視ユーザリストの準備 ################
Ignore_Users = [x.strip() for x in config.Ignore_Users]

# 無視ユーザリストのユーザ名を全部小文字にする
Ignore_Users = [str.lower() for str in Ignore_Users]

# 無視テキストリストの準備 ################
Ignore_Line = [x.strip() for x in config.Ignore_Line]

# 無視単語リストの準備 ################
Delete_Words = [x.strip() for x in config.Delete_Words]

# suffixのチェック、google_trans_newインスタンス生成
if hasattr(config, 'GoogleTranslate_suffix'):
    if config.GoogleTranslate_suffix not in URL_SUFFIX_LIST:
        url_suffix = 'co.jp'
    else:
        url_suffix = config.GoogleTranslate_suffix
else:
    url_suffix = 'co.jp'

translator = AsyncTranslator(url_suffix=url_suffix)
tts = tts.TTS(config)
sound = sound.Sound(config)

##########################################
# 関連関数 ################################
##########################################

#####################################
# Google Apps Script 翻訳
async def GAS_Trans(session, text, lang_source, lang_target):
    if text is None:
        config.Debug: print("[GAS_Trans] text is empty")
        return False

    url = config.GAS_URL
    payload = {
        "text"  : text,
        "source": lang_source,
        "target": lang_target
    }
    headers = {
        'Content-Type': 'application/json',
    }

    async with session.post(url, json=payload, headers=headers) as res:
        if res.status == 200:
            if config.Debug: print("[GAS_Trans] post success!")
            return await res.text()
        else:
            if config.Debug: print("[GAS_Trans] post failed...")
        return False

async def non_twitch_emotes(channel:str):
    emotes_list = [] # List of non-Twitch emotes
    conn = hc("emotes.adamcy.pl") # non-Twitch emotes API
    # Get non-Twitch channel emotes
    for path in [f"/v1/channel/{channel}/emotes/bttv.7tv.ffz","/v1/global/emotes/bttv.7tv.ffz"]:
        conn.request("GET", path) # Get non-Twitch emotes
        resp = conn.getresponse() # Get API response
        try:
            for i in json.loads(resp.read()):
                if re.match(r"[0-9][psmz]", i['code']):
                    continue
                if re.match(r"(chi|pon|kan|kita|riichi|ron|tsumo|toitoi|mleague)", i['code']):
                    continue
                if re.match(r"(hi|eyes|lychee|sleep|sleepy|MSQ|mentor|PonCat|Yo|doomed|confused|food|lurk)", i['code']):
                    continue
                if re.match(r"(raised|blind|Bio|Protect|Stoneskin|ShroudOfSaints|Bane|LuminiferousAether|FeyWind|FeyCaress|Contagion|Kardia|ClericStance)", i['code']):
                    continue
                if re.match(r"(astrologian|dancer|ninja|paladin|samurai|summoner|warrior|whitemage|blackmage|darkknight|gunbreaker|machinist|reaper|bluemage|dragoon|redmage|scholar|sage)", i['code']):
                    continue
                if re.match(r"(GLA|PLD|MRD|WAR|DRK|GNB|CNJ|WHM|SCH|AST|SAG|PGL|MNK|SAM|LNC|DRG|REA|ROG|NIN|ARC|BRD|MCH|DNC|THM|BLM|ACN|SMN|RDM|BLU|CRP|BSM|ARM|GSM|LTW|WVR|ALC|CUL|MIN|BTN|FSH)", i['code']):
                    continue
                
                emotes_list.append(i['code'])
        except Exception:
            pass
    return emotes_list

##########################################
# メイン動作 ##############################
##########################################

class Bot(commands.Bot):
    pi_tts_text = ""
    po_tts_text = ""
    p_out_text = ""

    def __init__(self):
        super().__init__(
            token               = config.Trans_OAUTH,
            prefix              = config.Bot_Prefix,
            initial_channels    = [config.Twitch_Channel, config.Trans_Target_Channel]
        )

    # 起動時 ####################
    async def event_channel_joined(self, channel):
        'Called once when the bot goes online.'
        print(f"{self.nick} joined {channel.name}!")
        self.output = self.get_channel(config.Trans_Username)
        
        await channel.send(f"Translating messages from this channel to https://twitch.tv/{config.Trans_Username}/chat Übersetze Nachrichten aus diesem Channel in https://twitch.tv/{config.Trans_Username}/chat …")

    # メッセージを受信したら ####################
    async def event_message(self, msg):
        'Runs every time a message is sent in chat.'

        # # bot自身の投稿は無視 -----------------
        if config.Debug: print(f'echo: {msg.echo}, {msg.content}')
        if msg.echo:
            return

        # コマンド処理 -----------------------
        if not msg.echo:
            await self.handle_commands(msg)

        if msg.content.startswith('!') or msg.content.startswith(config.Bot_Prefix):
            return
        if msg.channel.name == config.Trans_Target_Channel:
            return
        # 変数入れ替え ------------------------
        message = msg.content
        user    = msg.author.name.lower()
        non_twitch_emote_list = await non_twitch_emotes(config.Twitch_Channel) or await non_twitch_emotes(config.Twitch_Channel) or []

        # 無視ユーザリストチェック -------------
        if config.Debug: print('USER:{}'.format(user))
        if user in Ignore_Users:
            return

        # 無視テキストリストチェック -----------
        for w in Ignore_Line:
            if w in message:
                return

        # emoteの削除 --------------------------
        # エモート抜き出し
        emote_list = []
        # Twitch Emotes
        if msg.tags:
            if msg.tags['emotes']:
                # エモートの種類数分 '/' で分割されて提示されてくる
                emotes_s = msg.tags['emotes'].split('/')
                for emo in emotes_s:
                    if config.Debug: print()
                    if config.Debug: print(emo)
                    e_id, e_pos = emo.split(':')

                    # 同一エモートが複数使われてたら，その数分，情報が入ってくる
                    # （例：1110537:4-14,16-26）
                    if config.Debug: print(f'e_pos:{e_pos}')
                    if ',' in e_pos:
                        ed_pos = e_pos.split(',') # ed_pos = "emote duplicate position"?
                        for e in ed_pos:
                            if config.Debug: print(f'{e}')
                            if config.Debug: print(e.split('-'))
                            e_s, e_e = e.split('-') # e_s = "emote start", e_e = "emote end"
                            if config.Debug: print(msg.content[int(e_s):int(e_e)+1])

                            # リストにエモートを追加
                            emote_list.append(msg.content[int(e_s):int(e_e)+1])

                    else:
                        e = e_pos
                        e_s, e_e = e.split('-')
                        if config.Debug: print(msg.content[int(e_s):int(e_e)+1])

                        # リストにエモートを追加
                        emote_list.append(msg.content[int(e_s):int(e_e)+1])

        # en:Remove non-Twitch emotes from message     ja:メッセージからTwitch以外のエモートを削除
        temp_msg = message.split(' ')
        # en:Place non-Twitch emotes in temporary variable  ja:Twitch以外のエモートを一時的な変数に配置する。
        nte = list(set(non_twitch_emote_list) & set(temp_msg)) # nte = "non-Twitch emotes"
        for i in nte:
            if config.Debug: print(i)
            emote_list.append(i)
        # en:Place unicode emoji in temporary variable  ja:ユニコード絵文字をテンポラリ変数に入れる
        uEmoji = distinct_emoji_list(message) # uEmoji = "Unicode Emoji"
        for i in uEmoji:
            if config.Debug: print(i)
            emote_list.append(i)

        # message(msg.contextの編集用変数)から，エモート削除
        if config.Debug: print(f'message with emote:{message}')
        for w in sorted(emote_list, key=len, reverse=True):
            if config.Debug: print(w)
            message = message.replace(w, '')

        if config.Debug: print(f'message without emote:{message}')

        # 削除単語リストチェック --------------
        for w in Delete_Words:
            message = message.replace(w, '')

        # @ユーザー名を削除
        message = re.sub(r'@\S+', '', message)

        # 複数空文字を一つにまとめる --------
        message = " ".join( message.split() )

        if not message:
            return

        # 入力 --------------------------
        in_text = message
        print(f"{user}: {in_text}")
        if config.Trans_Target_Channel != config.Twitch_Channel:
            if not self.output:
                self.output = self.get_channel(config.Trans_Target_Channel)
            await self.output.send('{}: {}'.format(user, in_text))

        # 言語検出 -----------------------
        if config.Debug: print(f'--- Detect Language ---')
        lang_detect = 'un'

        # use google_trans_new ---
        if not config.GAS_URL or config.Translator == 'deepl':
            try:
                detected = await translator.detect(in_text)
                lang_detect = detected[0]
            except Exception as e:
                if config.Debug: print(e)

        # use GAS ---
        else:
            try:
                trans_text = await GAS_Trans(self._http.session, in_text, '', config.lang_TransToHome)
                if trans_text == in_text:
                    lang_detect = config.lang_TransToHome
                else:
                    lang_detect = 'GAS'
            except Exception as e:
                if config.Debug: print(e)

        if config.Debug: print(f'lang_detect:{lang_detect}')

        # 翻訳先言語の選択 ---------------
        if config.Debug: print(f'--- Select Destination Language ---')
        lang_dest = config.lang_TransToHome if lang_detect != config.lang_TransToHome else config.lang_HomeToOther
        if config.Debug: print(f"lang_detect:{lang_detect} lang_dest:{lang_dest}")

        # 翻訳先言語が文中で指定されてたら変更 -------
        m = in_text.split(':')
        if len(m) >= 2:
            if m[0] in TargetLangs:
                lang_dest = m[0]
                in_text = ':'.join(m[1:])
        else:
            # 翻訳先が (:)で指定されてなくて、
            # なおかつ 無視対象言語だったら全部無視して終了↑ ---------
            if lang_detect in Ignore_Lang:
                return

        if config.Debug: print(f"lang_dest:{lang_dest} in_text:{in_text}")

        # 音声合成（入力文） --------------
        # if len(in_text) > int(config.TooLong_Cut):
        #     in_text = in_text[0:int(config.TooLong_Cut)]
        if config.TTS_In:
            tts_text = in_text
            if lang_detect == "en" or lang_detect == "un":
                for pair in config.TTS_Substitutions['en']:
                    if config.Debug: print("Replacing \"" + pair[0] + "\" with \"" + pair[1] +"\"")
                    tts_text = re.sub(pair[0], pair[1], tts_text)
            else:
                if lang_detect in config.TTS_Substitutions: 
                    for pair in config.TTS_Substitutions[lang_detect]:
                        if config.Debug: print("Replacing \"" + pair[0] + "\" with \"" + pair[1] +"\"")
                        tts_text = re.sub(pair[0], pair[1], tts_text)
            if self.pi_tts_text != tts_text:
                print(f"TTS({lang_detect}): {tts_text}")
                tts.put(tts_text, lang_detect)
            else:
                print("Duplicate TTS detected. Ignoring…")
            self.pi_tts_text = tts_text

        # 検出言語と翻訳先言語が同じだったら無視！
        if lang_detect == lang_dest:
            return

        ################################
        # 翻訳 --------------------------
        if config.Debug: print(f'--- Translation ---')
        translatedText = ''

        # en:Use database to reduce deepl limit     
        # ja:データベースの活用でDeepLの字数制限を軽減
        translation_from_database = await db.get(in_text,lang_dest) if in_text is not None else None

        if translation_from_database is not None:
            translatedText = translation_from_database[0]
            if config.Debug: print(f'[Local Database](SQLite database file)')
        elif (translation_from_database is None) and (in_text is not None):
            # use deepl --------------
            # (try to use deepl, but if the language is not supported, text will be translated by google!)
            if config.Translator == 'deepl':
                try:
                    if lang_detect in deepl_lang_dict.keys() and lang_dest in deepl_lang_dict.keys():
                        translatedText = (
                            await asyncio.gather(asyncio.to_thread(deepl.translate, source_language=deepl_lang_dict[lang_detect], target_language=deepl_lang_dict[lang_dest], text=in_text))
                            )[0]
                        if config.Debug: print(f'[DeepL Tlanslate]({deepl_lang_dict[lang_detect]} > {deepl_lang_dict[lang_dest]})')
                    elif lang_detect == "un" and config.lang_Fallback in deepl_lang_dict.keys() and lang_dest in deepl_lang_dict.keys():
                        translatedText = (
                            await asyncio.gather(asyncio.to_thread(deepl.translate, source_language=deepl_lang_dict[config.lang_Fallback], target_language=deepl_lang_dict[lang_dest], text=in_text))
                            )[0]
                        if config.Debug: print(f'[DeepL Tlanslate]({deepl_lang_dict[config.lang_Fallback]} > {deepl_lang_dict[lang_dest]})')
                    else:
                        if not config.GAS_URL:
                            try:
                                translatedText = await translator.translate(in_text, lang_dest)
                                if config.Debug: print('[Google Tlanslate (google_trans_new)]')
                            except Exception as e:
                                if config.Debug: print(e)
                        else:
                            try:
                                translatedText = await GAS_Trans(self._http.session, in_text, '', lang_dest)
                                if config.Debug: print('[Google Tlanslate (Google Apps Script)]')
                            except Exception as e:
                                if config.Debug: print(e)
                except Exception as e:
                    if config.Debug: print(e)

            # NOT use deepl ----------
            elif config.Translator == 'google':
                # use google_trans_new ---
                if not config.GAS_URL:
                    try:
                        translatedText = await translator.translate(in_text, lang_dest)
                        if config.Debug: print('[Google Tlanslate (google_trans_new)]')
                    except Exception as e:
                        if config.Debug: print(e)

                # use GAS ---
                else:
                    try:
                        translatedText = await GAS_Trans(self._http.session, in_text, '', lang_dest)
                        if config.Debug: print('[Google Tlanslate (Google Apps Script)]')
                    except Exception as e:
                        if config.Debug: print(e)

            else:
                print(f'ERROR: config TRANSLATOR is set the wrong value with [{config.Translator}]')
                return

            if translatedText == "" or translatedText == in_text:
                if config.Debug: print('[Translation faulty, retrying with Google Translate]')
                try:
                    translatedText = await translator.translate(in_text, lang_dest)
                    if config.Debug: print('[Google Tlanslate (google_trans_new)]')
                except Exception as e:
                    if config.Debug: print(e)

            if translatedText != in_text: await db.save(in_text, translatedText, lang_dest)

        # チャットへの投稿 ----------------
        # 投稿内容整形 & 投稿
        out_text = translatedText
        if out_text.casefold().strip() == in_text.casefold().strip() or out_text.casefold().strip() == self.p_out_text.casefold().strip():
            if config.Debug: print(out_text)
            out_text = ""
            print("Input text equals output text, skipping line.")
        
        else:
            if out_text.strip():
                if config.Show_ByLang:
                    out_text = '{} ({} > {})'.format(out_text, lang_detect, lang_dest)
                if config.Show_ByName:
                    out_text = '{}: {}'.format(user, out_text)

            # コンソールへの表示 --------------
            print(out_text)

            # en:If message is only emoji; then do not translate, and do not send a message
            # ja:メッセージが絵文字だけの場合は、翻訳せず、メッセージを送らないでください
            if in_text is not None:
                if config.Trans_Target_Channel != config.Twitch_Channel:
                    if not self.output:
                        self.output = self.get_channel(config.Trans_Target_Channel)
                    await self.output.send("/me " + out_text)
                else:
                    await msg.channel.send("/me " + out_text)
                self.p_out_text = out_text

            # 音声合成（出力文） --------------
            # if len(translatedText) > int(config.TooLong_Cut):
            #     translatedText = translatedText[0:int(config.TooLong_Cut)]
            if out_text.casefold().strip() == in_text.casefold().strip():
                tts_text = in_text
                for pair in config.TTS_Substitutions[config.lang_Fallback]:
                    if config.Debug: print("Replacing \"" + pair[0] + "\" with \"" + pair[1] +"\"")
                    tts_text = re.sub(pair[0], pair[1], tts_text)
                
                print(f"TTS ({config.lang_Fallback}): {tts_text}")
                tts.put(tts_text, config.lang_Fallback)
            
            if config.TTS_Out and lang_dest in config.ReadOnlyTheseLang and out_text:
                tts_text = translatedText
                
                if lang_dest in config.TTS_Substitutions:
                    for pair in config.TTS_Substitutions[lang_dest]:
                        if config.Debug: print("Replacing \"" + pair[0] + "\" with \"" + pair[1] +"\"")
                        tts_text = re.sub(pair[0], pair[1], tts_text)

                if self.po_tts_text != tts_text:
                    print(f"TTS({lang_dest}): {tts_text}")
                    tts.put(tts_text, lang_dest)
                else:
                    print("Duplicate TTS detected. Ignoring…")
                
                self.po_tts_text = tts_text


# メイン処理 ###########################
def main():
    try:
        # 初期表示 -----------------------
        print('twitchTransFreeNext (Version: {})'.format(version))
        print('Connect to the channel   : {}'.format(config.Twitch_Channel))
        print('Translator Username      : {}'.format(config.Trans_Username))
        print('Translator ENGINE        : {}'.format(config.Translator))

        if not config.GAS_URL:
            print('Google Translate         : translate.google.{}'.format(url_suffix))
        else:
            print(f'Translate using Google Apps Script')
            if config.Debug: print(f'GAS URL: {config.GAS_URL}')

        if config.Debug: print("making tmp dir...")
        if os.path.exists(TMP_DIR):
            shutil.rmtree(TMP_DIR)

        os.mkdir(TMP_DIR)
        if config.Debug: print("made tmp dir.")

        # 音声合成スレッド起動 ################
        tts.run()

        # 音声再生スレッド起動 ################
        sound.run()

        # bot
        bot = Bot()
        bot.run()

    except Exception as e:
        if config.Debug: print(e)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
    db.close()
    db.delete()
