import os
import configparser

def get_access_token():

    # Construct the path to the config.ini file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, 'config.ini')

    try:
        config = configparser.ConfigParser()
        config.read(config_path)
        access_token = config.get('DEFAULT', 'access_token_profile')
        return access_token
    except (IOError, configparser.Error, KeyError) as e:
        raise ValueError(f"Error retrieving access token: {e}")

if __name__ == "__main__":
    access_token = get_access_token()
    print(access_token)
