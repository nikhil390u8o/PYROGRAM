




async def help_handle(client, msg):
  await msg.edit("Fetching commands...")
  data = fetch_commands()
  if not data:
    await msg.edit(f"No data found.")
    return
  
  
  sorted_keys = sorted(data.keys(), key=lambda x: x.lower())
  msg_lines = ["Commands"]
  for key in sorted_keys:
    desc = data[key]
    msg_lines.append(f"//{key} - {desc}")
  
  msg_to_send = "\n".join(msg_lines)
  await msg.edit(f"```{msg_to_send}```")
  
  





import requests
from config import FIREBASE

def fetch_commands():
    url = f"{FIREBASE}/userbot/commands.json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None