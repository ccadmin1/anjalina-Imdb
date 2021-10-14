import os
import time
import random
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from info import START_MSG, CHANNELS, ADMINS, AUTH_CHANNEL, CUSTOM_FILE_CAPTION
from utils import Media, get_file_details
from pyrogram.errors import UserNotParticipant
from db.mongo import insert, getid
logger = logging.getLogger(__name__)

PHOTO = [
    "https://telegra.ph/file/d053a8e9ef4ed93df38a0.jpg",
    "https://telegra.ph/file/d1c6ee6d32e142f3674ed.jpg", 
    "https://telegra.ph/file/8fd7710ee17bd34a963a5.jpg", 
    "https://telegra.ph/file/ecb7510e187f0e3b60852.jpg", 
    "https://telegra.ph/file/ef7f1cbc33ac9ee47578d.jpg", 
    "https://telegra.ph/file/a5ce5774734d8c119c630.jpg"
]

@Client.on_message(filters.private & filters.user(ADMINS) & filters.command(["broadcast"]))
async def broadcast(bot, message):
 if (message.reply_to_message):
   ms = await message.reply_text("Geting All ids from database ...........")
   ids = getid()
   tot = len(ids)
   await ms.edit(f"Starting Broadcast .... \n Sending Message To {tot} Users")
   for id in ids:
     try:
     	await message.reply_to_message.copy(id)
     except:
     	pass


@Client.on_message(filters.command("start"))
async def start(bot, cmd):
    usr_cmdall1 = cmd.text
    if usr_cmdall1.startswith("/start subinps"):
        if AUTH_CHANNEL:
            invite_link = await bot.create_chat_invite_link(int(AUTH_CHANNEL))
            try:
                user = await bot.get_chat_member(int(AUTH_CHANNEL), cmd.from_user.id)
                if user.status == "kicked":
                    await bot.send_message(
                        chat_id=cmd.from_user.id,
                        text="Sorry Sir, You are Banned to use me.",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                ident, file_id = cmd.text.split("_-_-_-_")
                await bot.send_photo(
                    chat_id=cmd.from_user.id,
                    photo=f"{random.choice(PHOTO)}",
                    caption="** 🔊 𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 🤭\n\n🔊 ഞങ്ങളുടെ 𝙈𝙖𝙞𝙣 𝘾𝙝𝙖𝙣𝙣𝙚𝙡 ജോയിൻ ചെയ്താൽ മാത്രമേ സിനിമ ലഭിക്കുകയുള്ളൂ.... 😁\n\nJoin ചെയ്ത ശേഷം Try Again ബട്ടൺ ക്ലിക്ക് ചെയ്യൂ.😁 **",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("💢 JOIN OUR CHANNEL 💢", url=invite_link.invite_link)
                            ],
                            [
                                InlineKeyboardButton(" 🔄 Try Again", callback_data=f"checksub#{file_id}")
                            ]
                        ]
                    ),
                    parse_mode="markdown"
                )
                return
            except Exception:
                await bot.send_message(
                    chat_id=cmd.from_user.id,
                    text="Something went Wrong.",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        try:
            ident, file_id = cmd.text.split("_-_-_-_")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{files.file_name}"
                user_id = int(cmd.from_user.id)
                insert(user_id)
                buttons = [
                    [
                        InlineKeyboardButton('💢 Join Channel 💢', url='https://t.me/cinemacollections')
                    ]]
                await bot.send_cached_media(
                    chat_id=cmd.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
        except Exception as err:
            await cmd.reply_text(f"Something went wrong!\n\n**Error:** `{err}`")
    elif len(cmd.command) > 1 and cmd.command[1] == 'subscribe':
        invite_link = await bot.create_chat_invite_link(int(AUTH_CHANNEL))
        await bot.send_photo(
            chat_id=cmd.from_user.id,
            photo=f"{random.choice(PHOTO)}",
            caption="**Please Join My Updates Channel to use this Bot!**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("💢 Join Channel 💢", url=invite_link.invite_link)
                    ]
                ]
            )
        )
    else:
        await cmd.reply_photo(
            photo=f"{random.choice(PHOTO)}",
            caption=START_MSG,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔍 𝖲𝖾𝖺𝗋𝖼𝗁 𝖧𝖾𝗋𝖾 🔎", switch_inline_query_current_chat=''),
                        InlineKeyboardButton("🗯 Ｇｒｏｕｐ 🗯", url="https://t.me/movieReqGroup1")
                    ],
                    [
                        InlineKeyboardButton("🦹‍♂️ Ｄｅｖ 🦹‍♀️", url="https://t.me/Anjalinas"),
                        InlineKeyboardButton("⚙️ Ａｂｏｕｔ ⚙️", callback_data="about")
                    ]    
                ]
            )
         )


@Client.on_message(filters.command('channel') & filters.user(ADMINS))
async def channel_info(bot, message):
    """Send basic information of channel"""
    if isinstance(CHANNELS, (int, str)):
        channels = [CHANNELS]
    elif isinstance(CHANNELS, list):
        channels = CHANNELS
    else:
        raise ValueError("Unexpected type of CHANNELS")

    text = '📑 **Indexed channels/groups**\n'
    for channel in channels:
        chat = await bot.get_chat(channel)
        if chat.username:
            text += '\n@' + chat.username
        else:
            text += '\n' + chat.title or chat.first_name

    text += f'\n\n**Total:** {len(CHANNELS)}'

    if len(text) < 4096:
        await message.reply(text)
    else:
        file = 'Indexed channels.txt'
        with open(file, 'w') as f:
            f.write(text)
        await message.reply_document(file)
        os.remove(file)


@Client.on_message(filters.command('total') & filters.user(ADMINS))
async def total(bot, message):
    """Show total files in database"""
    msg = await message.reply("Processing...⏳", quote=True)
    try:
        total = await Media.count_documents()
        await msg.edit(f'📁 Saved files: {total}')
    except Exception as e:
        logger.exception('Failed to check total files')
        await msg.edit(f'Error: {e}')


@Client.on_message(filters.command('logger') & filters.user(ADMINS))
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('TelegramBot.log')
    except Exception as e:
        await message.reply(str(e))


@Client.on_message(filters.command('delete') & filters.user(ADMINS))
async def delete(bot, message):
    """Delete file from database"""
    reply = message.reply_to_message
    if reply and reply.media:
        msg = await message.reply("Processing...⏳", quote=True)
    else:
        await message.reply('Reply to file with /delete which you want to delete', quote=True)
        return

    for file_type in ("document", "video", "audio"):
        media = getattr(reply, file_type, None)
        if media is not None:
            break
    else:
        await msg.edit('This is not supported file format')
        return

    result = await Media.collection.delete_one({
        'file_name': media.file_name,
        'file_size': media.file_size,
        'mime_type': media.mime_type
    })
    if result.deleted_count:
        await msg.edit('File is successfully deleted from database')
    else:
        await msg.edit('File not found in database')
@Client.on_message(filters.command('about'))
async def bot_info(bot, message):
    buttons = [
        [
            InlineKeyboardButton('💢 Ｃｈａｎｎｅｌ 💢', url='https://t.me/cinemacollections'),
            InlineKeyboardButton('🗯 Ｇｒｏｕｐ 🗯', url='https://t.me/movieReqGroup1')
        ]
        ]
    await message.reply(text="<b>Developer : <a href='https://t.me/Anjalinas'>Aɴᴊᴀʟɪɴᴀ</a>\nCode : <a href='https://t.me/Dhashamoolam_Dhamu'>Ɗнαѕнαмσσℓαм</a>\nLanguage : <code>Python3</code>\nLibrary : <a href='https://docs.pyrogram.org/'>Pyrogram asyncio</a>\nSource Code : <a href='tg://settings'>Cʟɪᴄᴋ Mᴇ</a>\nCʜᴀɴɴᴇʟ : <a href='https://t.me/cinemacollections'>Ｃｈａｎｎｅｌ</a> </b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

@Client.on_message(filters.command('help'))
async def bot_info(bot, message):
    buttons = [
        [
            InlineKeyboardButton('💢 Ｃｈａｎｎｅｌ 💢', url='https://t.me/Cinemacollections'),
            InlineKeyboardButton('🗯 Ｇｒｏｕｐ 🗯', url='https://t.me/movieReqGroup1')
        ]
        ]
    await message.reply(text="<b>If You Have Any Doubts And If Any Errors In Codes Or Bugs Inform Us On Our Support Group ❗️\n Use Below Buttons To Get Support Group / Update channel Links </b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

@Client.on_message(filters.command('info') & (filters.private | filters.group))
async def showinfo(client, message):
    try:
        cmd, id = message.text.split(" ", 1)
    except:
        id = False
        pass

    if id:
        if (len(id) == 10 or len(id) == 9):
            try:
                checkid = int(id)
            except:
                await message.reply_text("__Enter a valid USER ID__", quote=True, parse_mode="md")
                return
        else:
            await message.reply_text("__Enter a valid USER ID__", quote=True, parse_mode="md")
            return           

        if Config.SAVE_USER == "yes":
            name, username, dcid = await find_user(str(id))
        else:
            try:
                user = await client.get_users(int(id))
                name = str(user.first_name + (user.last_name or ""))
                username = user.username
                dcid = user.dc_id
            except:
                name = False
                pass

        if not name:
            await message.reply_text("__USER Details not found!!__", quote=True, parse_mode="md")
            return
    else:
        if message.reply_to_message:
            name = str(message.reply_to_message.from_user.first_name\
                    + (message.reply_to_message.from_user.last_name or ""))
            id = message.reply_to_message.from_user.id
            username = message.reply_to_message.from_user.username
            dcid = message.reply_to_message.from_user.dc_id
        else:
            name = str(message.from_user.first_name\
                    + (message.from_user.last_name or ""))
            id = message.from_user.id
            username = message.from_user.username
            dcid = message.from_user.dc_id
    
    if not str(username) == "None":
        user_name = f"@{username}"
    else:
        user_name = "none"

    await message.reply_text(
        f"<b><u>UserInfo</b></u>\n\n"
        f"<b>Name</b> : {name}\n"
        f"<b>UserID</b> : <code>{id}</code>\n"
        f"<b>Username Name</b> : {user_name}\n"
        f"<b>Permanant USER Link</b> : <a href='tg://user?id={id}'>Link ❗️</a>\n\n"
        f"<b>@MovieReqGroup1</b>",
        quote=True,
        parse_mode="html"
    )

@Client.on_message(filters.command('id') & (filters.private | filters.group))
async def showid(client, message):
    chat_type = message.chat.type

    if chat_type == "private":
        user_id = message.chat.id
        await message.reply_text(
            f"Your ID : `{user_id}`",
            parse_mode="md",
            quote=True
        )
    elif (chat_type == "group") or (chat_type == "supergroup"):
        user_id = message.from_user.id
        chat_id = message.chat.id
        if message.reply_to_message:
            reply_id = f"Replied User ID : `{message.reply_to_message.from_user.id}`"
        else:
            reply_id = ""
        await message.reply_text(
            f"Your ID : `{user_id}`\nThis Group ID : `{chat_id}`\n\n{reply_id}",
            parse_mode="md",
            quote=True
        )  

