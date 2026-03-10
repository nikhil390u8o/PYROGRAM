






async def save_handle(client, msg):
  text = msg.text or ""
  parts = text.split(maxsplit=1)
  command = parts[0] if len(parts) > 0 else ""
  value = parts[1] if len(parts) > 1 else ""
  chat_id = msg.chat.id
  my_msg_id = msg.id
  
  if msg.reply_to_message:
    reply_msg = msg.reply_to_message
    from_chat = reply_msg.chat.id
    msg_id = reply_msg.id
    await client.forward_messages(
            chat_id="me",  
            from_chat_id=from_chat,
            message_ids=msg_id
        )
    await msg.delete()
  else:
    await msg.edit("Reply to a message to save it to your Saved Messages.")