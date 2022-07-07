import os
import logging
from pyrogram import Client, filters
from telegraph import upload_file
from config import Config
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

Jebot = Client(
   "Telegraph Uploader",
   api_id=Config.APP_ID,
   api_hash=Config.API_HASH,
   bot_token=Config.TG_BOT_TOKEN,
)

@Jebot.on_message(filters.command("start"))
async def start(client, message):
   if message.chat.type == 'private':
       await Jebot.send_message(
               chat_id=message.chat.id,
               text="""<b>Hello 👋 there! I can upload photos,videos & gif animations to telegraph and provide you the link.

 Send me /help for more info.

A project by @Lakshan_Pathum</b>""",   
                            reply_markup=InlineKeyboardMarkup(
                                [[
                                        InlineKeyboardButton(
                                            "✍️Help👨‍💻", callback_data="help"),
                                        InlineKeyboardButton(
                                            "✅Channel✅", url="https://t.me/Lakshan_Pathum")
                                    ],[
                                      InlineKeyboardButton(
                                            "📦Source Code📦", url="https://github.com/supunmadurangasl/TelegraphBot")
                                    ]]
                            ),        
            disable_web_page_preview=True,        
            parse_mode="html")

@Jebot.on_message(filters.command("help"))
async def help(client, message):
    if message.chat.type == 'private':   
        await Jebot.send_message(
               chat_id=message.chat.id,
               text="""<b>Telegraph Bot Help!

😅 It is not complicated!

🔴 Just send me any photo,video or a gif animation with a file size which is less than 5mb.

🔴 Then wait for me to upload it to telegraph and send you the link.

A project by @Lakshan_Pathum</b>""",
        reply_markup=InlineKeyboardMarkup(
                                [[
                                        InlineKeyboardButton(
                                            " 🔙  Back 🔙", callback_data="start"),
                                        InlineKeyboardButton(
                                            " 🌀About 🌀", callback_data="about"),
                                  ],[
                                        InlineKeyboardButton(
                                            "📦 Source Code 📦", url="https://github.com/supunmadurangasl/TelegraphBot")
                                    ]]
                            ),        
            disable_web_page_preview=True,        
            parse_mode="html")

@Jebot.on_message(filters.command("about"))
async def about(client, message):
    if message.chat.type == 'private':   
        await Jebot.send_message(
               chat_id=message.chat.id,
               text="""<b>About Telegraph Bot!</b>

<b>🔥 Developer:</b> <a href="https://t.me/Lakshan_Pathum">Lakshan</a>

<b>🔥 Contact Me:</b> <a href="https://t.me/Lakshan_Pathum_Bot">My Assistant</a>

<b>🔥 Library:</b> <a href="https://github.com/pyrogram/pyrogram">Pyrogram</a>""",
     reply_markup=InlineKeyboardMarkup(
                                [[
                                        InlineKeyboardButton(
                                            "🔙  Back 🔙  ", callback_data="help"),
                                        InlineKeyboardButton(
                                            "📦Source Code 📦", url="https://github.com/supunmadurangasl/TelegraphBot")
                                    ]]
                            ),        
            disable_web_page_preview=True,        
            parse_mode="html")

@Jebot.on_message(filters.photo)
async def telegraphphoto(client, message):
    msg = await message.reply_text(" 📤 Uploading To Telegraph...")
    download_location = await client.download_media(
        message=message, file_name='root/jetg')
    try:
        response = upload_file(download_location)
    except:
        await msg.edit_text("Photo size should be less than 5mb!") 
    else:
        await msg.edit_text(f'**📤Uploaded To Telegraph!\n\n👉 https://telegra.ph{response[0]}\n\nJoin @slbotzone**',
            disable_web_page_preview=True,
        )
    finally:
        os.remove(download_location)

@Jebot.on_message(filters.video)
async def telegraphvid(client, message):
    msg = await message.reply_text("📤 Uploading To Telegraph...")
    download_location = await client.download_media(
        message=message, file_name='root/jetg')
    try:
        response = upload_file(download_location)
    except:
        await msg.edit_text("Video size should be less than 5mb!") 
    else:
        await msg.edit_text(f'**📤 Uploaded To Telegraph!\n\n👉 https://telegra.ph{response[0]}\n\nJoin @slbotzone**',
            disable_web_page_preview=True,
        )
    finally:
        os.remove(download_location)

@Jebot.on_message(filters.animation)
async def telegraphgif(client, message):
    msg = await message.reply_text("📤 Uploading To Telegraph...")
    download_location = await client.download_media(
        message=message, file_name='root/jetg')
    try:
        response = upload_file(download_location)
    except:
        await msg.edit_text("Gif size should be less than 5mb!") 
    else:
        await msg.edit_text(f'**📤 Uploaded To Telegraph!\n\n👉 https://telegra.ph{response[0]}\n\nJoin @slbotzone**',
            disable_web_page_preview=True,
        )
    finally:
        os.remove(download_location)

@Jebot.on_callback_query()
async def button(bot, update):
      cb_data = update.data
      if "help" in cb_data:
        await update.message.delete()
        await help(bot, update.message)
      elif "about" in cb_data:
        await update.message.delete()
        await about(bot, update.message)
      elif "start" in cb_data:
        await update.message.delete()
        await start(bot, update.message)

print(
    """
Bot Started!
Join @slbotzone
"""
)

Jebot.run()
