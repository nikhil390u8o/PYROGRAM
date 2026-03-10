from telethon import events
import re
from bot.clone import clone_handle
from bot.gen import gen_handle
from bot.start import start_handle
from bot.ping import ping_handle
from bot.send import send_handle
from bot.log import log_msg
from bot.addhelp import addhelp_handle

def register_bot(client):
  @client.on(events.NewMessage())
  async def handle_user_messages(event):
    if event.out:
        return
    await log_msg(client, event)
    
  @client.on(events.NewMessage(pattern=r"^/addhelp(\s.*)?$"))
  async def addhelp_cmd(event):
    await addhelp_handle(client, event)
    
  @client.on(events.NewMessage(pattern=r"^/start(\s.*)?$"))
  async def start_cmd(event):
    await start_handle(client, event)
    
  @client.on(events.NewMessage(pattern=r"^/clone(\s.*)?$"))
  async def clone_cmd(event):
    await clone_handle(client, event)
  
  @client.on(events.NewMessage(pattern=r"^/gen(\s.*)?$"))
  async def gen_cmd(event):
    await gen_handle(client, event)
  
  @client.on(events.NewMessage(pattern=r"^/ping(\s.*)?$"))
  async def ping_cmd(event):
    await ping_handle(client, event)
  
  @client.on(events.NewMessage(pattern=r"^/send(\s.*)?$"))
  async def send_cmd(event):
    await send_handle(client, event)