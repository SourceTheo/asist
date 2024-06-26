# Translate code for Theo edit by: @Source_Theo 

from asyncio import sleep

from googletrans import LANGUAGES, Translator

from . import BOTLOG, BOTLOG_CHATID, deEmojify

TRT_LANG = "en"


@bot.on(admin_cmd(pattern="ترجمه (.*)"))
@bot.on(sudo_cmd(pattern="ترجمه (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if "trim" in event.raw_text:
        return
    input_str = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str or "en"
    elif ";" in input_str:
        lan, text = input_str.split(";")
    else:
        await edit_delete(
            event, "⪼ **للترجمه رد على الرساله واكتب .ترجمه مع كود الدوله**", time=5
        )
        return
    text = deEmojify(text.strip())
    lan = lan.strip()
    Translator()
    try:
        translated = await getTranslate(text, dest=lan)
        after_tr_text = translated.text
        output_str = f"⪼ **تمت الترجمه من ↫ {LANGUAGES[translated.src].title()} الى {LANGUAGES[lan].title()} :**\
                \n\n{after_tr_text}"
        await edit_or_reply(event, output_str)
    except Exception as exc:
        await edit_delete(event, str(exc), time=5)


@bot.on(admin_cmd(outgoing=True, pattern=r"trt(?: |$)([\s\S]*)"))
@bot.on(sudo_cmd(allow_sudo=True, pattern=r"trt(?: |$)([\s\S]*)"))
async def translateme(trans):
    Translator()
    textx = await trans.get_reply_message()
    message = trans.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await edit_or_reply(trans, "`Give a text or reply to a message to translate!`")
        return
    try:
        reply_text = await getTranslate(deEmojify(message), dest=TRT_LANG)
    except ValueError:
        await edit_delete(trans, "`Invalid destination language.`", time=5)
        return
    source_lan = LANGUAGES[f"{reply_text.src.lower()}"]
    transl_lan = LANGUAGES[f"{reply_text.dest.lower()}"]
    reply_text = f"**From {source_lan.title()}({reply_text.src.lower()}) to {transl_lan.title()}({reply_text.dest.lower()}) :**\n`{reply_text.text}`"

    await edit_or_reply(trans, reply_text)
    if BOTLOG:
        await trans.client.send_message(
            BOTLOG_CHATID,
            f"`Translated some {source_lan.title()} stuff to {transl_lan.title()} just now.`",
        )


@bot.on(admin_cmd(pattern="lang trt (.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="lang trt (.*)", allow_sudo=True))
async def lang(value):
    scraper = "Translator"
    global TRT_LANG
    arg = value.pattern_match.group(1).lower()
    if arg in LANGUAGES:
        TRT_LANG = arg
        LANG = LANGUAGES[arg]
    else:
        await edit_or_reply(
            value,
            f"`Invalid Language code !!`\n`Available language codes for TRT`:\n\n`{LANGUAGES}`",
        )
        return
    await edit_or_reply(value, f"`Language for {scraper} changed to {LANG.title()}.`")
    if BOTLOG:
        await value.client.send_message(
            BOTLOG_CHATID, f"`Language for {scraper} changed to {LANG.title()}.`"
        )


async def getTranslate(text, **kwargs):
    translator = Translator()
    result = None
    for _ in range(10):
        try:
            result = translator.translate(text, **kwargs)
        except Exception:
            translator = Translator()
            await sleep(0.1)
    return result


CMD_HELP.update(
    {
        "ترجمه": "**Plugin :** `ترجمه`\
         \n\n**  • Syntax : **`.ترجمه ar/en <text/reply>`\
         \n**  • Function : **Translates given language to destination language. For <text> use .tl LanguageCode ; <text>\
         \n\n**  • Syntax : **`.trt <Reply/text>`\
         \n**  • Function : **it will translate your messege\
         \n\n**  • Syntax : **`.lang trt LanguageCode`\
         \n**  • Function : **It will set default langaugeCode for **trt**\
         \n\n**  • Check here ** [Language codes](https://telegra.ph/Language-codes-11-01)\
        "
    }
)
