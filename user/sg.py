import aiohttp
from config import FIREBASE
import requests
import os


req = "Reply to a user or provide a username."
MAX_MSG_LENGTH = 4096

async def sg_handle(client, msg):
  chat_id = msg.chat.id
  text = msg.text  # e.g. "//sg username"
  parts = text.split(maxsplit=2)  # splits into words, max 2 splits
  command = parts[0] if len(parts) > 0 else None
  user = parts[1] if len(parts) > 1 else None
  
  user_id = None
  
  if not user and not msg.reply_to_message:
    await msg.edit(req)
    return
  
  if msg.reply_to_message:
    reply_msg = msg.reply_to_message.from_user
    user_id = reply_msg.id
    
  if not user_id:
    try:
      user = await client.get_users(user)
      user_id = user.id
    except Exception as e:
      await msg.edit(f"I haven't seen this user before.")
      return
  await msg.edit("Retrieving user information...")
  first_name, username = await fetch_user_data(user_id)
  
  if not first_name :
    await msg.edit(f"I haven't seen this user before.")
    return
  
  f_name_msg = "\n".join(first_name) + "\n" if first_name else ""
  u_name_msg = "\n".join(username) + "\n" if username else ""
  msg_to_send = f"""**➠ User History Info - Name**
{f_name_msg}
**➠ User History Info - Username**
{u_name_msg}
  """
  if len(msg_to_send) <= MAX_MSG_LENGTH:
    await msg.edit(f"{msg_to_send}")
  else:
    file_name = f"{user_id}.txt"
    with open(file_name, "w", encoding="utf-8") as f:
            f.write(msg_to_send)
    await client.send_document(chat_id, file_name)
    await msg.delete()
    os.remove(file_name)
  
  
  





async def fetch_user_data(user_id: str):
    url = f"{FIREBASE}/sg/{user_id}.json"  # fetch all under user_id

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return None, None
            data = await resp.json()

    if not data:
        return None, None

    f_name = []
    u_name = []

    # data is a dict of unknown keys, each value is dict with first_name, username etc.
    for item in data.values():
        if isinstance(item, dict):
            first_name = item.get("first_name")
            username = item.get("username")

            if first_name:
                f_name.append(first_name)
            if username:
                u_name.append(username)

    if not f_name and not u_name:
        return None, None

    return f_name, u_name


    
    

async def adsg_handle(client, msg):
  if not msg:
    return
  user = msg.from_user
  user_id = user.id
  first_name = user.first_name
  username = user.username if user.username else None
  
  data = {
    "first_name" : first_name,
    "username" : username,
    "user_id" : user_id
  }
  
  store_history(data)








import requests
from datetime import datetime
import pytz
from config import FIREBASE

def store_history(data):
    user_id = data.get("user_id")
    if not user_id:
        print("❌ user_id omission")
        return False

    base_url = f"{FIREBASE}/sg/{user_id}.json"

    try:
        # Fetch existing entries for user_id
        resp = requests.get(base_url)
        if resp.status_code != 200:
            print(f"❌ Failed to fetch existing data for user {user_id}")
            return False

        existing_data = resp.json() or {}

        # Prepare data without 'date' key for comparison
        new_entry = data.copy()
        new_entry.pop("date", None)

        # Check if identical entry exists
        for key, entry in existing_data.items():
            entry_compare = entry.copy()
            entry_compare.pop("date", None)
            if entry_compare == new_entry:
                print(f"♻️ Identical entry already exists under key {key}, no new entry added.")
                return True

        # Get current India time timestamp in seconds
        india_tz = pytz.timezone("Asia/Kolkata")
        now = datetime.now(india_tz)
        timestamp = str(int(now.timestamp()))  # seconds as string

        # Add new entry with timestamp key
        existing_data[timestamp] = new_entry

        # PUT updated dict back
        put_resp = requests.put(base_url, json=existing_data)
        if put_resp.status_code == 200:
            print(f"➕ Added new entry with timestamp key {timestamp}")
            return True
        else:
            print(f"❌ Failed to add new entry for user {user_id}")
            return False

    except Exception as e:
        print(f"❌ Exception in store_history: {e}")
        return False