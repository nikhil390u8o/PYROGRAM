






async def spam_handle(client, msg):
  text = msg.text
  chat_id = msg.chat.id
  parts = text.split(maxsplit=2)  
  command = parts[0] if len(parts) > 0 else ""
  times = parts[1] if len(parts) > 1 else ""
  value = parts[2] if len(parts) > 2 else ""
  
  x = None 
  
  if times == "":
    await msg.edit("Usage : `//spam 10 message `")
    return
  
  if times:
    try:
      x = int(times)
    except:
      await msg.edit("Second argument must be a numeric message count.")
      return
    
  if value == "":
    await msg.edit("The message can't be empty.")
    return
  
  await msg.delete()
  for i in range(x):
    await client.send_message(chat_id, value)
  

