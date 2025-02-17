import re
import base64
import logging
from struct import pack
from telegraph import upload_file
from pyrogram.errors import UserNotParticipant
from pyrogram.file_id import FileId
from pymongo.errors import DuplicateKeyError
from umongo import Instance, Document, fields
from marshmallow.exceptions import ValidationError
import os
import requests
import json
from info import DB2, COLLECTION_NAME

COLLECTION_NAME_2="groups"
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

instance = Instance.from_db(DB2)
imdb=Instance.from_db(DB2)

@instance.register
class Media(Document):
    id = fields.StrField(attribute='_id')
    text = fields.StrField(required=True)
    reply = fields.StrField(required=True)
    btn = fields.StrField(required=True)
    file = fields.StrField(required=True)
    alert = fields.StrField(required=True)
    type = fields.StrField(required=True)
    group_id = fields.IntField(required=True)
    descp = fields.StrField(required=True)
    price = fields.IntField(required=True)
    grp = fields.StrField(required=True)
    class Meta:
        collection_name = COLLECTION_NAME

@imdb.register
class User(Document):
    id = fields.IntField(attribute='_id')
    group_id= fields.IntField(required=True)
    status = fields.StrField(required=True)
    title = fields.StrField(required=True)
    link = fields.StrField(allow_none=True)
    inv_link = fields.StrField(required=True)
    total_m = fields.IntField(required=True)
    photo_id = fields.StrField(allow_none=True)
    class Meta:
        collection_name = COLLECTION_NAME_2

async def add_user(id, usr,sts,ttl):
    try:
        data = User(
            id = id,
            group_id= usr,
            status = sts,
            title = ttl,
            link=None,
            inv_link = 'hrn',
            total_m =0,
            photo_id = None
        )
    except ValidationError:
        logger.exception('Error occurred while saving group in database')
    else:
        try:
            await data.commit()
        except DuplicateKeyError:
            logger.warning("already saved in database")
        else:
            logger.info("group is saved in database")

async def save_file(text,reply,btn,file,alert,type,id,user_id,descp,prc,grp):
    """Save file in database"""
    text = str(text).lower()
    fdata = {'text': text}
    button = f'{btn}'
    button = button.replace('pyrogram.types.InlineKeyboardButton', 'InlineKeyboardButton')
    fdata['group_id'] = user_id
    found = await Media.find_one(fdata)
    if found:
        await Media.collection.delete_one(fdata)
    try:
        file = Media(
            id=id,
            text=text,
            reply=str(reply),
            btn=f'{button}',
            file= str(file),
            alert=str(alert),
            type=str(type),
            group_id =user_id,
            descp=descp,
            price = prc,
            grp = grp
       )
    except ValidationError:
        logger.exception('Error occurred while saving file in database')
    else:
        try:
            await file.commit()
        except DuplicateKeyError:
            logger.warning(text + " is already saved in database")
        else:
            logger.info(text + " is saved in database")

async def get_search_results(query, group_id, max_results=10, offset=0):
    """For given query return (results, next_offset)"""
    
    query = query.strip()
    if not query:
        raw_pattern = '.'
    elif ' ' not in query:
        raw_pattern = r'\b' + query + r'.*'
    else:
        raw_pattern = query.replace(' ', r'.*[\s\.\+\-_]')

    try:
        regex = re.compile(raw_pattern, flags=re.IGNORECASE)
    except:
        return []
    else:
        filter = {'text': regex}
    filter['group_id'] = group_id
    total_results = await Media.count_documents(filter)
    next_offset = offset + max_results

    if next_offset > total_results:
        next_offset = ''

    cursor = Media.find(filter)
    # Sort by recent
    cursor.sort('$natural', -1)
    # Slice files according to offset and max results
    cursor.skip(offset).limit(max_results)
    # Get list of files
    files = await cursor.to_list(length=max_results)

    return files, next_offset


async def get_filter_results(query,group_id):
    query = query.strip()
    if not query:
        raw_pattern = '.'
    elif ' ' not in query:
        raw_pattern = r'\b' + query + r'.*'
    else:
        raw_pattern = query.replace(' ', r'.*[\s\.\+\-_]')
    try:
        regex = re.compile(raw_pattern, flags=re.IGNORECASE)
    except:
        return []
    filter = {'text': regex}
    filter['group_id'] = group_id
    total_results = await Media.count_documents(filter)
    cursor = Media.find(filter)
    cursor.sort('$natural', -1)
    files = await cursor.to_list(length=int(total_results))
    return files

async def is_user_exist(query):
    filter = {'id': query}
    cursor = User.find(filter)
    
    userdetails = await cursor.to_list(length=1)
    return userdetails

async def is_group_exist(query):
    filter = {'status': query}
    cursor = User.find(filter)
    cursor.sort('$natural', -1)
    count = await User.count_documents(filter)
    userdetails = await cursor.to_list(length = int(count))
    return userdetails
async def get_file_details(query):
    filter = {'id': query}
    cursor = Media.find(filter)
    filedetails = await cursor.to_list(length=1)
    return filedetails
async def get_group_filters(query ,sts, max_results=10,offset=0):
    """For given query return (results, next_offset)"""

    query = query.strip()
    if not query:
        raw_pattern = '.'
    elif ' ' not in query:
        raw_pattern = r'\b' + query + r'.*'
    else:
        raw_pattern = query.replace(' ', r'.*[\s\.\+\-_]')
    try:
        regex = re.compile(raw_pattern, flags=re.IGNORECASE)
    except:
        return []

    filter = {'title': regex}
    filter['status'] = sts
    total_results = await User.count_documents(filter)
    next_offset = offset + max_results

    if next_offset > total_results:
        next_offset = ''

    cursor = User.find(filter)
    # Sort by recent
    cursor.sort('$natural', -1)
    # Slice files according to offset and max results
    cursor.skip(offset).limit(max_results)
    # Get list of files
    files = await cursor.to_list(length=max_results)

    return files, next_offset

async def upload_group(client, thumb,message):
  img_path = (f"./DOWNLOADS/{message.from_user.id}.jpg")
  if thumb:
    img_path = await client.download_media(message=thumb.big_file_id, file_name=img_path)
  else:
    return None
  try:
    tlink = upload_file(img_path)
  except:
    await msg.edit_text("`Something went wrong`")
    return None
  else: 
    os.remove(img_path)
  link2= f"https://telegra.ph{tlink[0]}"
  return link2
