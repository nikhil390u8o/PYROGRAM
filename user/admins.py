from pyrogram.enums import ChatType
from pyrogram import Client
from pyrogram.enums import ChatMembersFilter





async def admins_handle(client, msg):
  if msg.chat.type == ChatType.PRIVATE or msg.chat.type == ChatType.BOT:
    await msg.edit("Try on group chat.")
    return
  chat_id = msg.chat.id
  
  admins = []
  async for member in client.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
    user = member.user
    if not user.is_bot:   
      admins.append(user.mention)
  await msg.edit("Admins:\n" + "\n".join(admins))
  


async def bots_handle(client, msg):
  if msg.chat.type == ChatType.PRIVATE or msg.chat.type == ChatType.BOT:
    await msg.edit("Try on group chat.")
    return
  chat_id = msg.chat.id

  admin_bots = []
  async for member in client.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
    user = member.user
    if user.is_bot:
      admin_bots.append(user.mention)

  response = "Bots:\n"
  response += "\n".join(admin_bots) if admin_bots else "None"

  await msg.edit(response)
  


