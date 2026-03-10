import requests
from config import FIREBASE
from session import users



#insert data into firebase 
def add_user_to_database(data: dict):
    user_id = data.get("user_id")
    if not user_id:
        print("❌ user_id not found in data")
        return False
    
    url = f"{FIREBASE}/clients/{user_id}.json"
    response = requests.put(url, json=data)

    if response.status_code == 200:
        print("✅ Data added to Firebase successfully")
        return True
    else:
        print(f"❌ Failed to add data: {response.text}")
        return False
  
  




#fetch users from firebase
def fetch_sessions_from_database():
    try:
        # Get all users from Firebase
        response = requests.get(f"{FIREBASE}/clients.json")

        if response.status_code != 200 or response.json() is None:
            print("❌ Failed to fetch users or no data found.")
            return

        data = response.json()  # dictionary of user_id -> data

        # Check and create users["client"] if it doesn't exist
        if "client" not in users:
            users["client"] = []

        for user_id, user_data in data.items():
            session = user_data.get("string")
            if session and session not in users["client"]:
                users["client"].append(session)

        print("✅ Sessions loaded")

    except Exception as e:
        print(f"❌ Error while fetching sessions: {e}")


def add_new_user(data: dict):
    user_id = data.get("user_id")
    if not user_id:
        print("❌ user_id not found in data")
        return False
    
    url = f"{FIREBASE}/users/{user_id}.json"
    response = requests.put(url, json=data)

    if response.status_code == 200:
        print("✅ New user started")
        return True
    else:
        print(f"❌ Failed to add data: {response.text}")
        return False


def fetch_user():
    try:
        # Get all users from Firebase
        response = requests.get(f"{FIREBASE}/users.json")

        if response.status_code != 200 or response.json() is None:
            print("❌ Failed to fetch users or no data found.")
            return None

        data = response.json()  # dictionary of key -> value

        # Extract all keys from users
        keys_list = list(data.keys()) if isinstance(data, dict) else None

        return keys_list

    except Exception as e:
        print(f"❌ Error while fetching user keys: {e}")
        return None