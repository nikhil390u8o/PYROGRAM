import asyncio





async def type_handle(client, msg):
  
  command, value = msg.text.split(' ', 1) if ' ' in msg.text else (msg.text, '')
  
  if value == "":
    await msg.edit("Provide message after command")
    return
  
  val = len(value)
  
  if len(value) > 120:
    await msg.edit("msg is too long.")
    return
  
  cursor = "▌"
  text = value
  for i in range(1, len(value)):
    await msg.edit(text[:i] + cursor)
  await msg.edit(text)
  
  
  
  