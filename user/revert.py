from session import clone_users, users_info



async def revert_handle(client, msg):
  sender_id = msg.from_user.id
  
  current, pre = get_clone_data(sender_id)
  
  if not current and not pre:
    await msg.edit("There is no account to revert.")
    return
  
  if not pre:
    print(current)
    print(type(current))
    profile = current.get("profile")
    if profile:
      await delete_profile_photo(client)
    me = users_info.get(sender_id)
    first_name = me.get("first_name")
    try:
      await client.update_profile(first_name=first_name, last_name=None)
      await msg.edit("Reverted to original account ✅ ")
    except Exception as e:
      await msg.edit(f"{e}")
      return
  
  if pre and current:
    profile = current.get("profile")
    if profile:
      await delete_profile_photo(client)
    
    first_name = pre.get("first_name")
    user_id = pre.get("user_id")
    mention = f"[{first_name}](tg://user?id={user_id})"
    await msg.edit(f"Reverting back to {mention}'s account...")
    try:
      await client.update_profile(first_name=first_name, last_name=None)
      await msg.edit(f"Reverted to {mention}'s account ✅ ")
    except Exception as e:
      await msg.edit(f"{e}")
      return





async def delete_profile_photo(client):
    photos = []
    async for photo in client.get_chat_photos("me", limit=1):
        photos.append(photo)

    if not photos:
        print("No profile photos found.")
        return False

    latest_photo = photos[0]
    await client.delete_profile_photos(latest_photo.file_id)
    print("Deleted latest profile photo.")
    return True
    
def get_clone_data(user_id):
    # Agar user_id present nahi hai
  if user_id not in clone_users:
    return None, None
    
  data_list = clone_users[user_id]
  if not data_list:
    return None, None
    
  if len(data_list) == 1:
    data = data_list.pop()  # data ko list se nikal do
    return data, None
    
  last_data = data_list.pop()          
  second_last_data = data_list[-1]    
  return last_data, second_last_data