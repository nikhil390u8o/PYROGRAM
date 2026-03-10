import asyncio



opening = [
  "#include <iostream>  // Standard I/O for terminal hacking",
  "#include <string>    // Handle secret strings and keys",
  "#include <vector>    // Store decrypted data packets",
  "#include <ctime>     // Sync with system time for exploits",
  "#include <openssl/hmac.h>  // Secure cryptographic bypass",
  "#include <openssl/evp.h>   // Encryption and decryption toolkit",
  "// Initializing hack sequence...",
  "// Loading MTProto interception module...",
  "// Bypassing 2FA and OTP verification...",
  "// Extracting user session tokens...",
  "// Deploying stealth payloads...",
]
def get_hack(index):
  if index < 0 or index >= len(opening):
    return ""
  return "\n".join(opening[:index + 1])

import random

def gen_num():
  first_digit = str(random.randint(1, 9))
  other_digits = ''.join(str(random.randint(0, 9)) for _ in range(25))
  return first_digit + other_digits


async def hack_handle(client, msg, delay=0.5):
  total_length = 20  
  for percent in range(0, 11):
    hn = gen_num()
    hack_text = get_hack(percent)
    p = percent *10
    done_length = int(total_length * percent / 10)
    bar = "█" * done_length + "░" * (total_length - done_length)
    text = f"**Decrypting...{p}%** \n{bar}\n{hn}```console\n{hack_text}```"
    try:
      await msg.edit(text)
      await asyncio.sleep(delay)
    except Exception:
      break
    
  mention = None
  if msg.reply_to_message:
    reply_user = msg.reply_to_message.from_user
    user_id = reply_user.id
    first_name = reply_user.first_name or "User"
    mention = f"[{first_name}](tg://user?id={user_id})"
    
  if not mention:
    mention = "Targeted"
  
  hack_msg = f"""📱 {mention} Account Details:
🤝 Telegram Phone Number Accessed  
🔐 Password and OTP Bypass Achieved  
👾 Silent Session Login Established 
  """
  
  await msg.edit(hack_msg)
  