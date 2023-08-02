from datetime import datetime, timedelta
from asgiref.sync import async_to_sync
from django.conf import settings
from pyrogram import Client
from pyrogram.types import InputPhoneContact, ChatPrivileges, ChatMemberUpdated, ChatMember
import pathlib

api_id = settings.API_ID
api_hash = settings.API_HASH
app = Client("my_account", api_id=api_id, api_hash=api_hash)


async def main(phone: str):
    app = Client("my_account", api_id=api_id, api_hash=api_hash)
    async with app:
        another_contact = InputPhoneContact(phone, "Foo")
        have_user = await app.import_contacts([another_contact])
        contact = await app.get_contacts()
        for user in contact:
            if user.first_name == "Foo":
                await app.delete_contacts([user.id])
    return have_user


async def createGroup(name: str, first_post: str, users: list, photo):
    app = Client("my_account", api_id=api_id, api_hash=api_hash)
    async with app:
        chat = await app.create_group(name, users)
        for user in users:
            try:
                chat = await chat.add_members(user)
            except:
                continue
        await app.set_chat_photo(chat.id, photo=photo)
        await app.send_message(chat.id, first_post)
    return chat


async def updateGroup(chat_id: int, users: list):
    app = Client("my_account", api_id=api_id, api_hash=api_hash)
    async with app:
        chat = await app.get_chat(chat_id)
        member_ids = []
        async for member in chat.get_members():
            member_ids.append(member.user.id)
        for user in users:
            try:
                await chat.add_members(user)
            except:
                continue
        for member in member_ids:
            if member not in users:
                await app.ban_chat_member(chat_id, member, datetime.now() + timedelta(seconds=40))


async def leaveGroup(chat_id, users_id, admin_title: str = 'Ustoz'):
    app = Client("my_account", api_id=api_id, api_hash=api_hash)
    async with app:
        if users_id != []:
            chat_privileges = ChatPrivileges(can_delete_messages=True,
                                             can_manage_video_chats=True,
                                             can_restrict_members=True,
                                             can_promote_members=True,
                                             can_change_info=True,
                                             can_post_messages=True,
                                             can_edit_messages=True,
                                             can_invite_users=True,
                                             can_pin_messages=True)
            for user in users_id:
                try:
                    chat = await app.set_administrator_title(chat_id, user, admin_title)
                    if chat:
                        group = await app.promote_chat_member(chat_id, user, privileges=chat_privileges)
                    if group:
                        try:
                            await app.leave_chat(chat_id, True)
                        except:
                            return True
                except:
                    return True
    return True

create_group = async_to_sync(createGroup)
update_group = async_to_sync(updateGroup)
leave_group = async_to_sync(leaveGroup)
get_tgusers = async_to_sync(main)

# print(user)
