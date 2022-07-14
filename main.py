import os
import time
import math
import json
import string
import random
import traceback
import asyncio
import datetime
import aiofiles
from random import choice 
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid, UserNotParticipant, UserBannedInChannel
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid
from telegraph import upload_file
from database import Database

UPDATE_CHANNEL = os.environ.get("UPDATE_CHANNEL")
BOT_OWNER = int(os.environ["BOT_OWNER"])
DATABASE_URL = os.environ["DATABASE_URL"]
db = Database(DATABASE_URL, "Telegraph-Uploader")

Bot = Client(
    "Telegraph Uploader Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"],
)


@Bot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    
    if not await db.is_user_exist(update.from_user.id):
	    await db.add_user(update.from_user.id)
	   
        await Bot.send_message(
               chat_id=message.chat.id,
               text="""<b>Hello 👋 there! I can upload photos,videos & gif animations to telegraph and provide you the link.

 Send me /help for more info.

A project by @MR_SADUWA</b>""",   
                            reply_markup=InlineKeyboardMarkup(
                                [[
                                        InlineKeyboardButton(
                                            "✍️Help👨‍💻", callback_data="help"),
                                        InlineKeyboardButton(
                                            "✅Channel✅", url="https://t.me/MR_SADUWA")
                                    ],[
                                      InlineKeyboardButton(
                                            "📦Source Code📦", url="https://github.com/supunmadurangasl/TelegraphBot")
                                    ]]
                            ),        
            disable_web_page_preview=True,        
            parse_mode="html")

@Bot.on_message(filters.private & filters.command(["help"]))
async def help(bot, update):
    
    if not await db.is_user_exist(update.from_user.id):
	    await db.add_user(update.from_user.id)
    if message.chat.type == 'private':   
        await  Bot.send_message(
               chat_id=message.chat.id,
               text="""<b>Telegraph Bot Help!

😅 It is not complicated!

🔴 Just send me any photo,video or a gif animation with a file size which is less than 5mb.

🔴 Then wait for me to upload it to telegraph and send you the link.

A project by @MR_SADUWA</b>""",
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

@Bot.on_message(filters.private & filters.command(["about"]))
async def about(bot, update):
    
    if not await db.is_user_exist(update.from_user.id):
	    await db.add_user(update.from_user.id)
	    
    if message.chat.type == 'private':   
        await   Bot.send_message(
               chat_id=message.chat.id,
               text="""<b>About Telegraph Bot!</b>

<b>🔥 Developer:</b> <a href="https://t.me/MR_SADUWA">Saduwa</a>

<b>🔥 Contact Me:</b> <a href="https://t.me/t">My Assistant</a>

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

@Bot.on_message(filters.media & filters.private)
async def telegraph_upload(bot, update):
    
    if not await db.is_user_exist(update.from_user.id):
	    await db.add_user(update.from_user.id)
    
    if UPDATE_CHANNEL:
        try:
            user = await bot.get_chat_member(UPDATE_CHANNEL, update.chat.id)
            if user.status == "kicked":
                await update.reply_text(text="You are banned!")
                return
        except UserNotParticipant:
            await update.reply_text(
		  text=FORCE_SUBSCRIBE_TEXT,
		  reply_markup=InlineKeyboardMarkup(
			  [[InlineKeyboardButton(text="⚙ Join Updates Channel ⚙", url=f"https://t.me/szteambots")]]
		  )
	    )
            return
        except Exception as error:
            print(error)
            await update.reply_text(text="Something wrong. Contact <a href='https://t.me/InukaRanmira'>Developer</a>.", disable_web_page_preview=True)
            return
    
    text = await update.reply_text(
        text="<code>Downloading to My Server.....</code>",
        disable_web_page_preview=True
    )
    media = await update.download()
    
    await text.edit_text(
        text="<code>Downloading Completed. Now I am Uploading Your Photo/Video To Telegraph.....</code>",
        disable_web_page_preview=True
    )
    
    try:
        response = upload_file(media)
    except Exception as error:
        print(error)
        await text.edit_text(
            text=f"Error :- {error}",
            disable_web_page_preview=True
        )
        return
    
    try:
        os.remove(media)
    except Exception as error:
        print(error)
        return
    
    await text.edit_text(
        text=f"<b>Link :-</b> <code>https://telegra.ph{response[0]}</code>\n\n<b>Join :-</b> @szteambots",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Open Link🔗", url=f"https://telegra.ph{response[0]}"),
                    InlineKeyboardButton(text="Share Link🎁", url=f"https://t.me/share/url?url=https://telegra.ph{response[0]}"),
		    InlineKeyboardButton(text="☘️Join With Us", url=f"https://t.me/szteambots")
                ],
                [InlineKeyboardButton(text="⚙ Join Updates Channel ⚙", url="https://t.me/szteambots")]
            ]
        )
    )

@Bot.on_callback_query()

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


@Bot.on_message(filters.private & filters.command("broadcast") & filters.user(BOT_OWNER) & filters.reply)
async def broadcast(bot, update):
	broadcast_ids = {}
	all_users = await db.get_all_users()
	broadcast_msg = update.reply_to_message
	while True:
	    broadcast_id = ''.join([random.choice(string.ascii_letters) for i in range(3)])
	    if not broadcast_ids.get(broadcast_id):
	        break
	out = await update.reply_text(text=f"Broadcast Started! You will be notified with log file when all the users are notified.")
	start_time = time.time()
	total_users = await db.total_users_count()
	done = 0
	failed = 0
	success = 0
	broadcast_ids[broadcast_id] = dict(total = total_users, current = done, failed = failed, success = success)
	async with aiofiles.open('broadcast.txt', 'w') as broadcast_log_file:
	    async for user in all_users:
	        sts, msg = await send_msg(user_id = int(user['id']), message = broadcast_msg)
	        if msg is not None:
	            await broadcast_log_file.write(msg)
	        if sts == 200:
	            success += 1
	        else:
	            failed += 1
	        if sts == 400:
	            await db.delete_user(user['id'])
	        done += 1
	        if broadcast_ids.get(broadcast_id) is None:
	            break
	        else:
	            broadcast_ids[broadcast_id].update(dict(current = done, failed = failed, success = success))
	if broadcast_ids.get(broadcast_id):
	    broadcast_ids.pop(broadcast_id)
	completed_in = datetime.timedelta(seconds=int(time.time()-start_time))
	await asyncio.sleep(3)
	await out.delete()
	if failed == 0:
	    await update.reply_text(text=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.", quote=True)
	else:
	    await update.reply_document(document='broadcast.txt', caption=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.")
	os.remove('broadcast.txt')


@Bot.on_message(filters.private & filters.command("stats"), group=5)
async def status(bot, update):
    total_users = await db.total_users_count()
    text = "**Bot Status**\n"
    text += f"\n**Total Users:** `{total_users}`"
    await update.reply_text(
        text=text,
        quote=True,
        disable_web_page_preview=True
    )

Bot.run()
print("Bot Online Now✅")
