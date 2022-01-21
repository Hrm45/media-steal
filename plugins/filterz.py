from pyrogram import filters
from plugins.database import db
ADMINS = [859704527]
all_user=db.get_all_users()

def is_admin(_, __, update):
    try:
        user_id = update.from_user.id
    except:
        return False

    if user_id in ADMINS:
        return True
    else:
        return False

filters.admins = filters.create(is_admin)
admins=filters.admins
