from pyrogram import filters
from user.sg import sg_handle, adsg_handle
from user.fuck import fuck_handle
from user.hack import hack_handle
from user.save import save_handle
from user.set_profile import name_handle, username_handle, update_pfp, bio_handle
from user.clone import clone_handle
from user.revert import revert_handle
from user.help import help_handle
from user.spam import spam_handle
from user.type import type_handle
from user.ping import ping_handle
from user.love import loveyou_handle, love_handle
from user.loveyou import loveyou_handle
from user.lover import lover_handle
from user.dino import dino_anim


def register_user(client):
  @client.on_message(filters.outgoing & filters.regex(r'^//lover(?:\s|$)'))
  async def handle_spam(client, message):
    await lover_handle(client, message)
    
  @client.on_message(filters.outgoing & filters.regex(r'^//dino(?:\s|$)'))
  async def handle_spam(client, message):
    await dino_anim(client, message)
    
  @client.on_message(filters.outgoing & filters.regex(r'^//spam(?:\s|$)'))
  async def handle_spam(client, message):
    await spam_handle(client, message)
    
  @client.on_message(filters.outgoing & filters.regex(r'^//loveyou(?:\s|$)'))
  async def handle_lover(client, message):
    await loveyou_handle(client, message)
  
  @client.on_message(filters.outgoing & filters.regex(r'^//love(?:\s|$)'))
  async def handle_love(client, message):
    await love_handle(client, message)
    
  @client.on_message(filters.outgoing & filters.regex(r'^//ping(?:\s|$)'))
  async def handle_ping(client, message):
    await ping_handle(client, message)
    
  @client.on_message(filters.outgoing & filters.regex(r'^//type(?:\s|$)'))
  async def handle_type(client, message):
    await type_handle(client, message)
    
  @client.on_message(filters.outgoing & filters.regex(r'^//help(?:\s|$)'))
  async def handle_help(client, message):
    await help_handle(client, message)
    
  @client.on_message(filters.outgoing & filters.regex(r'^//revert(?:\s|$)'))
  async def handle_revert(client, message):
    await revert_handle(client, message)
  
  @client.on_message(filters.outgoing & filters.regex(r'^//clone(?:\s|$)'))
  async def handle_clone(client, message):
    await clone_handle(client, message)
    
  @client.on_message(filters.outgoing & filters.regex(r'^//setbio(?:\s|$)'))
  async def handle_bio(client, message):
    await bio_handle(client, message)
    
  @client.on_message(filters.outgoing & filters.regex(r'^//setpfp(?:\s|$)'))
  async def handle_pfp(client, message):
    await update_pfp(client, message)
    
  @client.on_message(filters.outgoing & filters.regex(r'^//setusername(?:\s|$)'))
  async def handle_username(client, message):
    await username_handle(client, message)
  
  @client.on_message(filters.outgoing & filters.regex(r'^//setname(?:\s|$)'))
  async def handle_name(client, message):
    await name_handle(client, message)
  
  @client.on_message(filters.outgoing & filters.regex(r'^//save(?:\s|$)'))
  async def handle_save(client, message):
    await save_handle(client, message)
    
  @client.on_message(filters.outgoing & filters.regex(r'^//hack(?:\s|$)'))
  async def handle_hack(client, message):
    await hack_handle(client, message)
  
  @client.on_message(filters.outgoing & filters.regex(r'^//fuck(?:\s|$)'))
  async def handle_fuck(client, message):
    await fuck_handle(client, message)
    
  @client.on_message(filters.outgoing & filters.regex(r'^//sg(?:\s|$)'))
  async def handle_sg(client, message):
    await sg_handle(client, message)
    
  @client.on_message(filters.incoming | filters.outgoing)
  async def handle_all_messages(client, message):
    await adsg_handle(client, message)
    
