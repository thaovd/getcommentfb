import os
import configparser
import requests

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

ACCESS_TOKEN_PROFILE = config.get('DEFAULT', 'ACCESS_TOKEN_PROFILE')
PAGE_ID = config.get('DEFAULT', 'PAGE_ID')

def get_profile_data():
    url = f"https://graph.facebook.com/v18.0/me?access_token={ACCESS_TOKEN_PROFILE}&fields=name,id"
    response = requests.get(url)
    
    if response.status_code == 200:
        profile_data = response.json()
        return {
            "name": profile_data["name"],
            "id": profile_data["id"]
        }
    else:
        return None

if __name__ == "__main__":
    profile_data = get_profile_data()
    if profile_data:
        print(f"Name: {profile_data['name']}")
        print(f"ID: {profile_data['id']}")
    else:
        print("Failed to fetch profile data.")
