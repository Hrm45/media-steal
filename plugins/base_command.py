from info import filters
from utils import get_file_details,get_filter_results
from pyrogram  import Client
from plugins.database import db
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from plugins.strings import START_MESSAGE, HELP_MESSAGE, ABOUT_MESSAGE, MARKDOWN_HELP

start_keyboard = [
    [
        InlineKeyboardButton(text = '🤔 Help', callback_data = "help"),
        InlineKeyboardButton(text = '🤖 About', callback_data = "about")
    ],
    [
        InlineKeyboardButton(text = 'Close 🔒', callback_data = "close"),
        InlineKeyboardButton(text = 'Search Here', switch_inline_query_current_chat = '')
    ]
]

start_keyboard_c = [
    [
        InlineKeyboardButton(text = '🤖 About', callback_data = "about"),
        InlineKeyboardButton(text = 'Close 🔒', callback_data = "close")
    ],
    [
        InlineKeyboardButton(text = 'Search Here', switch_inline_query_current_chat = '')
    ]
]

help_keyboard = [
    [
        InlineKeyboardButton(text = '✏️ Markdown Helper ✏️', callback_data = 'markdownhelper')
    ],
    [
        InlineKeyboardButton(text = '🤖 About', callback_data = 'about'),
        InlineKeyboardButton(text = 'Close 🔒', callback_data = 'close')
    ]
]

about_keyboard = [
     [
        InlineKeyboardButton(text = '🤔 Help', callback_data = 'help'),
        InlineKeyboardButton(text = 'Close 🔒', callback_data = 'close')
    ]
]

about_keyboard_c = [
    [
        InlineKeyboardButton(text = 'Close 🔒', callback_data = 'close')
    ]
]

markdown_keyboard = [
    [
        InlineKeyboardButton(text = '🔙 Back', callback_data = 'help')
    ]
]

@Client.on_message(filters.command('start') & filters.private)
async def start_msg_admins(client, message):
    if await db.is_admin_exist(message.from_user.id):
        reply_markup = InlineKeyboardMarkup(start_keyboard)
    else:
        reply_markup = InlineKeyboardMarkup(start_keyboard_c)
    text = START_MESSAGE.format(
        mention = message.from_user.mention,
        first_name = message.from_user.first_name,
        last_name = message.from_user.last_name,
        user_id = message.from_user.id,
        username = '' if message.from_user.username == None else '@'+message.from_user.username
    )
    usr_cmdall1 = message.text
    cmd=message
    if usr_cmdall1.startswith("/start subinps"):
        ban_status = await db.get_ban_status(cmd.from_user.id)  
        try:
            ident, file_id = cmd.text.split("_-_-_-_")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                f_caption=files.reply
                group_id = files.group_id
                
            if not await db.is_acc_all_exist(cmd.from_user.id,group_id):
                akg = await client.send_message(chat_id=cmd.from_user.id,text="Please wait")
            elif not await db.is_acc_exist(cmd.from_user.id,file_id):
                await client.send_message(
                        chat_id=cmd.from_user.id,
                        text=f"Samahani **{cmd.from_user.first_name}** nmeshindwa kukuruhusu kendelea kwa sababu muv au sizon uliochagua ni za kulipia\n Tafadhal chagua nchi uliopo kuweza kulipia uweze kuitazama",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton("🇹🇿 TANZANIA", callback_data =f"tanzania {file_id}"),
                                    InlineKeyboardButton("🇰🇪 KENYA",callback_data ="kenya" )
                                ]
                            ]
                        )
                    )
                return
            await akg.delete()
            strg=files.descp.split('.dd#.')[3]
            if filedetails:
                if filedetails:
                    if strg.lower() == 'm':
                        filez=await get_filter_results(file_id,group_id)
                        for file in reversed(filez):
                            filedetails = await get_file_details(file.id)
                            for files in filedetails:
                                f_caption=files.reply
                                await client.send_cached_media(
                                    chat_id=cmd.from_user.id,
                                    file_id=files.file,
                                    caption=f_caption
                                )
                        return
                    elif strg.lower() == 's':
                        link = files.descp.split('.dd#.')[2]
                        f_caption =f'\n🌟 @Bandolako2bot \n\n **💥Series  zetu zote zipo google drive, Kama huwezi kufungua link zetu tafadhali bonyeza 📪 ADD EMAIL kisha fuata maelekezo**'
                        await client.send_photo(
                            chat_id=cmd.from_user.id,
                            photo=files.file,
                            caption=f_caption,
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📪 ADD EMAIL",callback_data = "addemail")],[InlineKeyboardButton("🔗 GOOGLE LINK",url= link)]])
                        )
                        return
                     
                else:
                    await client.send_message(
                        chat_id=cmd.from_user.id,
                        text=f"Samahani **{cmd.from_user.first_name}** nmeshindwa kukuruhusu kendelea kwa sababu muv au sizon uliochagua ni za kulipia\n Tafadhal chagua nchi uliopo kuweza kulipia kifurushi",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton("🇹🇿 TANZANIA", callback_data = "tanzania"),
                                    InlineKeyboardButton("🇰🇪 KENYA",callback_data ="kenya" )
                                ]
                            ]
                        )
                    )
                    return
        except Exception as err:
            await cmd.reply_text(f"Something went wrong!\n\n**Error:** `{err}`")
    else:
        await message.reply(
            text = text,
            quote = True,
            reply_markup = reply_markup,
            disable_web_page_preview = True
        )
    
@Client.on_message(filters.command('help') & filters.private)
async def help_msg(client, message):
    await message.reply(
        text = HELP_MESSAGE,
        quote = True,
        reply_markup = InlineKeyboardMarkup(help_keyboard)
    )

@Client.on_message(filters.command('about') & filters.private)
async def about_msg(client, message):
    user_id = message.from_user.id
    if await db.is_admin_exist(user_id):
        reply_markup = InlineKeyboardMarkup(about_keyboard)
    else:
        reply_markup = InlineKeyboardMarkup(about_keyboard_c)
    await message.reply(
        text = ABOUT_MESSAGE,
        quote = True,
        reply_markup = reply_markup,
        disable_web_page_preview = True
    )

@Client.on_callback_query(filters.regex(r'^close$'))
async def close_cbb(client, query):
    try:
        await query.message.reply_to_message.delete()
    except:
        pass
    try:
        await query.message.delete()
    except:
        pass

@Client.on_callback_query(filters.regex(r'^help$'))
async def help_cbq(client, query):
    await query.edit_message_text(
        text = HELP_MESSAGE,
        reply_markup = InlineKeyboardMarkup(help_keyboard)
    )
    
@Client.on_callback_query(filters.regex('^about$'))
async def about_cbq(client, query):
    user_id = query.from_user.id
    if await db.is_admin_exist(user_id):
        reply_markup = InlineKeyboardMarkup(about_keyboard)
    else:
        reply_markup = InlineKeyboardMarkup(about_keyboard_c)
    await query.edit_message_text(
        text = ABOUT_MESSAGE,
        reply_markup = reply_markup,
        disable_web_page_preview = True
    )
    
@Client.on_callback_query(filters.regex('^markdownhelper$'))
async def md_helper(client, query):
    await query.edit_message_text(
        text = MARKDOWN_HELP,
        reply_markup = InlineKeyboardMarkup(markdown_keyboard),
        disable_web_page_preview = True,
        parse_mode = 'html'
    )
@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except:
        typed = query.from_user.id
        pass
    if (clicked == typed):
        if query.data == "kenya":
            await query.answer()
            mkv = await client.ask(text = " Samahani sana wateja wetu wa Kenya bado hatuja weka utaratibu mzuri.\n  hivi karibun tutaweka mfumo mzuri ili muweze kupata huduma zetu", chat_id = query.from_user.id)
        
        elif query.data.startwith("tanzania"):
            await query.answer()
            fileid = query.data.split(" ",1)[1]
            await query.message.delete()
            filedetails = await get_file_details(fileid)
            for files in filedetails:
                f_caption=files.reply
                group_id = files.group_id
                fileid = files.file
                type1 = files.type
            if type1=="photo":
                await client.send_photo(
                            chat_id=query.from_user.id,
                            photo= fileid,
                            caption =f'text="🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿\n** VIFURUSHI VYA SWAHILI GROUP** \n🔴 wiki 1(07 days) ➡️ 2000/= \n\n🟠 wiki 2(14 days) ➡️ 3000/= \n\n🟡 wiki 3(21 days) ➡️ 4000/= \n\n🟢 mwezi (30 days) ➡️ 5000/= \n\n↘️Lipa kwenda **0624667219** halopesa:Ukishafanya malipo bonyeza button nmeshafanya malipo\n **__KARIBUN SANA SWAHILI GROUP__**",reply_markup=InlineKeyboardMarkup([[InlineKeyboardBa movie", callback_data=f"malipo {group_id} {fileid}")]])' )
            else:
                await client.send_cached_media(
                                    chat_id=query.from_user.id,
                                    file_id=fileid,
                                    caption=f'text="🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿\n** VIFURUSHI VYA SWAHILI GROUP** \n🔴 wiki 1(07 days) ➡️ 2000/= \n\n🟠 wiki 2(14 days) ➡️ 3000/= \n\n🟡 wiki 3(21 days) ➡️ 4000/= \n\n🟢 mwezi (30 days) ➡️ 5000/= \n\n↘️Lipa kwenda **0624667219** halopesa:Ukishafanya malipo bonyeza button nmeshafanya malipo\n **__KARIBUN SANA SWAHILI GROUP__**",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔴 malipo ya movie", callback_data=f"malipo {group_id} {fileid}")]])'
                                )
        elif query.data.startwith("malipo"):
            await query.answer()
            msg1 = query.data.split(" ")[1]
            msg2 = query.data.split(" ")[2]
            await query.message.delete()
            mkv = await client.ask(text='🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿\nTuma screenshot ya malipo yako kisha subir kidogo wasimamiz wangu wahakiki muamala wako',chat_id = query.from_user.id,reply_markup=ForceReply())
            if mkv.photo:
                await client.send_message(chat_id = query.from_user.id,text='🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿\ntumepokea screenshot ngoja tuihakiki tutakupa majibu tukimaliza')
                await client.send_photo(
                            chat_id=msg1,
                            photo= mkv.photo.file_id,
                            caption =f'id = {query.from_user.id}\n Name :message.from_user.first_name}' ,
                            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Activate", callback_data=f"yes {query.from_user.id} {msg2}"),InlineKeyboardButton("chat private", URL=f"tg://user?id={query.from_user.id}")]]))
            else:
                await mkv.delete()
                await client.send_message(chat_id = query.from_user.id,text = " Nmelazimika kukurudisha hapa kwa sababu umetuma ujumbe sio sahihi\n🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿\n** VIFURUSHI VYA SWAHILI GROUP** \n🔴 wiki 1(07 days) ➡️ 2000/= \n\n🟠 wiki 2(14 days) ➡️ 3000/= \n\n🟡 wiki 3(21 days) ➡️ 4000/= \n\n🟢 mwezi (30 days) ➡️ 5000/= \n\n↘️Lipa kwenda **0624667219** halopesa:Ukishafanya malipo bonyeza button nmeshafanya malipo\n **__KARIBUN SANA SWAHILI GROUP__**",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔴 Nmeshafanya malipo", callback_data=f"malipo {msg1} {msg2}")]]))
        elif query.data.startwith("yes"):
            msg0 = query.data.split(" ")[1]
            msg2 = query.data.split(" ")[2]
            await query.edit_message_photo(
                    photo = query.message.photo.file_id,
                    caption = f'je unauhakika tumruhusu {query.from_user.first_name} bonyeza ndiyo kukubali au bonyeza rudi kurudi kwenye screenshot ya muamala',
                    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("ndiyo", callback_data="ndiyo {msg1} {msg2}"),InlineKeyboardButton("rudi ", callback_data=f"malipo {query.from_user.id} {msg2}")]]),
                )
        elif query.data.startswith("0"):
            msg1=query.data.split(" ")[1]
            msg0=query.data.split(" ")[0]
            if msg0=="0":
                msg0="0"
            else:
                msg0+="0"
            await query.edit_message_text(
                    text = f'{query.message.text}\n{msg1} {msg0}',
                    reply_markup = InlineKeyboardMarkup([[]]),
                )
     
        elif query.data.startswith("1"):
            elif query.data.startswith("0"):
            msg1=query.data.split(" ")[1]
            msg0=query.data.split(" ")[2]
            if msg0=="0":
                msg0="1"
            else:
                msg0+="1"
            await query.edit_message_text(
                    text = f'{query.message.text}\n{msg1} {msg0}',
                    reply_markup = InlineKeyboardMarkup([[]]),
                )
        elif query.data.startswith("2"):
            elif query.data.startswith("0"):
            msg1=query.data.split(" ")[1]
            msg0=query.data.split(" ")[2]
            if msg0=="0":
                msg0="2"
            else:
                msg0+="2"
            await query.edit_message_text(
                    text = f'{query.message.text}\n{msg1} {msg0}',
                    reply_markup = InlineKeyboardMarkup([[]]),
                )
        elif query.data.startswith("3"):
            elif query.data.startswith("0"):
            msg1=query.data.split(" ")[1]
            msg0=query.data.split(" ")[0]
            if msg0=="0":
                msg0="3"
            else:
                msg0+="3"
            msg2 = query.data.split(" ")[2]
            if msg2=="c":
                await query.edit_message_caption(
                        text = f'{query.message.text.split('msg1')[0]}\n{msg1} {msg0}',
                        reply_markup = InlineKeyboardMarkup([[]]),
                    )
            elif msg2=="t":
                await query.edit_message_text(
                        text = f'{query.message.text}\n{msg1} {msg0}',
                        reply_markup = InlineKeyboardMarkup([[]]),
                    )
        elif query.data.startswith("4"):
            elif query.data.startswith("0"):
            msg1=query.data.split(" ")[1]
            msg0=query.data.split(" ")[2]
            if msg0=="0":
                msg0="4"
            else:
                msg0+="4"
            await query.edit_message_text(
                    text = f'{query.message.text}\n{msg1} {msg0}',
                    reply_markup = InlineKeyboardMarkup([[]]),
                )
        elif query.data.startswith("5"):
            elif query.data.startswith("0"):
            msg1=query.data.split(" ")[1]
            msg0=query.data.split(" ")[2]
            if msg0=="0":
                msg0="5"
            else:
                msg0+="5"
            await query.edit_message_text(
                    text = f'{query.message.text}\n{msg1} {msg0}',
                    reply_markup = InlineKeyboardMarkup([[]]),
                )
        elif query.data.startswith("6"):
            elif query.data.startswith("0"):
            msg1=query.data.split(" ")[1]
            msg0=query.data.split(" ")[2]
            if msg0=="0":
                msg0="6"
            else:
                msg0+="6"
            await query.edit_message_text(
                    text = f'{query.message.text}\n{msg1} {msg0}',
                    reply_markup = InlineKeyboardMarkup([[]]),
                )
        elif query.data.startswith("7"):
            elif query.data.startswith("0"):
            msg1= query.data.split(" ")[1]
            msg0= query.data.split(" ")[2]
            if msg0=="0":
                msg0="7"
            else:
                msg0+="7"
            msg2 = query.data.split(" ")[3]
            if msg2=="c":
                await query.edit_message_caption(
                        text = f'{query.message.text}\n{msg1} {msg0}',
                        reply_markup = InlineKeyboardMarkup([[]]),
                    )
            elif msg2=="t":
                await query.edit_message_text(
                        text = f'{query.message.text}\n{msg1} {msg0}',
                        reply_markup = InlineKeyboardMarkup([[]]),
                    )
            
        elif query.data.startswith("8"):
            elif query.data.startswith("0"):
            msg1=query.data.split(" ")[1]
            msg0=query.data.split(" ")[2]
            if msg0=="0":
                msg0="8"
            else:
                msg0+="8"
            await query.edit_message_text(
                    text = f'{query.message.text}\n{msg1} {msg0}',
                    reply_markup = InlineKeyboardMarkup([[]]),
                )
        elif query.data.startswith("9"):
            elif query.data.startswith("0"):
            msg1=query.data.split(" ")[1]
            msg0=query.data.split(" ")[2]
            if msg0=="0":
                msg0="9"
            else:
                msg0+="9"
            await query.edit_message_text(
                    text = f'{query.message.text}\n{msg1} {msg0}',
                    reply_markup = InlineKeyboardMarkup([[]]),
                )
        elif query.data.startswith("00"):
            elif query.data.startswith("0"):
            msg1=query.data.split(" ")[1]
            msg0=query.data.split(" ")[2]
            if msg0=="0":
                msg0="0"
            else:
                msg0+="00"
            await query.edit_message_text(
                    text = f'{query.message.text}\n{msg1} {msg0}',
                    reply_markup = InlineKeyboardMarkup([[]]),
                )
        elif query.data.startswith("000"):
            elif query.data.startswith("0"):
            msg1=query.data.split(" ")[1]
            msg0=query.data.split(" ")[2]
            if msg0=="0":
                msg0="0"
            else:
                msg0+="000"
            await query.edit_message_text(
                    text = f'{query.message.text}\n{msg1} {msg0}',
                    reply_markup = InlineKeyboardMarkup([[]]),
                )
        elif query.data.startswith("delete"):
            elif query.data.startswith("0"):
            msg1=query.data.split(" ")[1]
            await query.edit_message_text(
                    text = f'{query.message.text}\n{msg1} 0',
                    reply_markup = InlineKeyboardMarkup([[]]),
                )
def replymkup(msg7,txt1):
    reply1 = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("1", callback_data="malipo"),
                InlineKeyboardButton("2", callback_data="malipo"),
                InlineKeyboardButton("3", callback_data="malipo"),
                InlineKeyboardButton("4", callback_data="malipo"),
                InlineKeyboardButton("5", callback_data="malipo")
            ],
            [
                InlineKeyboardButton("6", callback_data="malipo"),
                InlineKeyboardButton("7", callback_data="malipo"),
                InlineKeyboardButton("8", callback_data="malipo"),
                InlineKeyboardButton("9", callback_data="malipo"),
                InlineKeyboardButton("x", callback_data="malipo")
            ],
            [
                InlineKeyboardButton("🔴 Nmeshafanya malipo", callback_data="malipo"),
                InlineKeyboardButton("🔴 Nmeshafanya malipo", callback_data="malipo")
            ]
        ]))
