from telethon import events
from config import API_ID, API_HASH
import asyncio

from pyrogram import Client




from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded
import asyncio



async def gen_handle(client, event):
    
    
    
    chat_id = event.chat.id
    
    # Step 1: Phone number
    await event.reply("📱 Send your phone number with country code (e.g. +91...)")
    phone = await listen(client, chat_id)
    if not phone:
        return
    
    # Create temp client (no console input)
    new_client = Client(
        "temp",
        api_id=API_ID,
        api_hash=API_HASH,
        in_memory=True
    )
    
    sent = await event.respond("Sending code...")
    await new_client.connect()
    try:
      sent_code = await new_client.send_code(phone)
    except Exception as e:
      await sent.edit(f"Invalid phone number.")
      return
    # Step 2: OTP
    await sent.edit("📩 Send the OTP you received (e.g., 1 2 3 4 5)")
    code = await listen(client, chat_id)
    
    try:
        await new_client.sign_in(phone_number=phone, phone_code_hash=sent_code.phone_code_hash, phone_code=code)
    except SessionPasswordNeeded:
        await event.respond("🔒 Your account has 2FA enabled. Send your password:")
        password = await listen(client, chat_id)
        try:
          await new_client.check_password(password=password)
        except Exception as e:
          await event.respond("Wrong password! Try again in a moment.")
          return
    except Exception as e:
      await event.respond("Oops! That OTP doesn’t seem right.")
      return
    
    # Export session string
    session_str = await new_client.export_session_string()
    await event.respond(f"<blockquote><b>Session generated ✅  </b></blockquote>\n<code>{session_str}</code>", parse_mode="html")
    
    await new_client.disconnect()

# `listen` function ko tumhe implement karna hoga jo user ka agla message return kare.








async def listen(client, chat_id):
    loop = asyncio.get_event_loop()
    future = loop.create_future()

    @client.on(events.NewMessage(chats=chat_id))
    async def handler(event):
        if event.text and event.text.startswith("/"):
            print("Command detected, exiting listener.")
        else:
            if not future.done():
                future.set_result(event.raw_text)

        client.remove_event_handler(handler)

    try:
        # Wait for message or timeout (5 minutes = 300 seconds)
        result = await asyncio.wait_for(future, timeout=300)
    except asyncio.TimeoutError:
        print("Timeout: No message received in 5 minutes.")
        result = None
        client.remove_event_handler(handler)

    return result