import time



clone_users = {}

#session storage
users = {}
users_info = {}
ping = {}







def my_profile(user):
  user_id = user.id
  first_name = user.first_name
  last_name = user.last_name
  username = user.username
  phone = user.phone_number
  
  users_info[user_id] = {
    "first_name" : first_name,
    "last_name": last_name,
    "username": username,
    "phone": phone
  }
  
  print(f"Started userbot: {user.first_name} (@{user.username})")

def set_ping():
  ts = int(time.time())
  ping["time"] = ts
  print("Ping has been set.")