from config import SUDO_USERS
import asyncio
import requests
from config import FIREBASE



async def addhelp_handle(client, event):
  
  sender_id = event.sender_id
  chat_id = event.chat_id
  if sender_id not in SUDO_USERS:
    return
  
  msg = """OK. Send me a list of commands for your userbot. Please use this format:

command1 - Description
command2 - Another description"""
  await event.respond(msg)
  res = await listen_message_in_chat(client, chat_id)
  
  if res == False:
    return
  
  if res == None:
    await event.respond("Send text only.")
    return
  
  co, de = parse_commands(res)
  
  if not co and not de:
    await event.respond("Please follow the format.")
    return
  
  data = {f"{cmd}": desc for cmd, desc in zip(co, de)}
  sent = await event.respond("Uploading commands...")
  add = upload_commands(data)
  if add:
    await sent.edit("Userbot commands set successfully! ✅")
    return
  else:
    await sent.edit(f"Error uploading command.")
  
  
  
  
  



def parse_commands(res: str):
    co = []
    de = []
    
    lines = res.strip().split('\n')
    if not lines:
        return None, None

    for line in lines:
        if ' - ' not in line:
            return None, None # Format mismatch
        parts = line.split(' - ', 1)
        if len(parts) != 2:
            return None, None
        command, desc = parts[0].strip(), parts[1].strip()
        if not command or not desc:
            return None, None
        co.append(command)
        de.append(desc)
    
    if co and de:
        return co, de
    else:
        return None, None



import asyncio
from telethon import events

async def listen_message_in_chat(client, chat_id, timeout=300):
    future = asyncio.get_running_loop().create_future()

    @client.on(events.NewMessage(chats=chat_id))
    async def handler(event):
        client.remove_event_handler(handler)
        message = event.message
        if message.text:
            future.set_result(message.text)
        else:
            future.set_result(None)

    # Ensure client is connected
    if not client.is_connected():
        await client.start()

    try:
        result = await asyncio.wait_for(future, timeout=timeout)
        return result
    except asyncio.TimeoutError:
        client.remove_event_handler(handler)
        return False






import requests
from config import FIREBASE

def upload_commands(data):
    url = f"{FIREBASE}/userbot/commands.json"   # / zaroori hai yahan
    try:
        response = requests.patch(url, json=data)   # patch use kiya
        if response.status_code == 200:
            print("Data uploaded successfully!")
            return True
        else:
            print(f"Failed to upload data. Status code: {response.status_code}")
            print("Response:", response.text)
            return False
    except Exception as e:
        print(f"Exception occurred: {e}")
        return False