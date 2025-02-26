import tvdb
import os
import re

def rename_file_with_tvdb_id(BEARER, TVDB_ID, FILE_PATH):
    if not TVDB_ID.isnumeric():
        return False

    fpsplit = FILE_PATH.split("/")
    filename = fpsplit[-1]
    filedir_path = "/".join(fpsplit[:-1])
    print(f"Processing file: {filename}")

    filename_data = tvdb.parse_filename_data(filename)
    if filename_data is None: return False
    if filename_data["season_number"] is not None: return True
    print("filename_data: ", filename_data)
    season_number = filename_data["season_number"]
    episode_number = filename_data["episode_number"]

    # If the season+episode numbers are unknown then ask TVDB for it
    if season_number is None:
        se_numbers = tvdb.get_season_episode_numbers(BEARER, TVDB_ID, episode_number)
        if se_numbers is None: return False
        season_number = se_numbers["season_number"]
        episode_number = se_numbers["episode_number"]


    season_number_str = tvdb.season_zerofill(season_number)
    episode_number_str = tvdb.episode_zerofill(episode_number)


    def resub_replace(match):
        return match.group(0).replace(match.group(1), f"S{season_number_str}E{episode_number_str}")

    new_filename = re.sub(r'[a-zA-Z0-9!\.\?, ]* - ([a-zA-Z0-9]*) +', resub_replace, filename)

    print(new_filename)

    new_file_path = f"{filedir_path}/{new_filename}"
    print(f"new_file_path: {new_file_path}")

    # Rename the file finally and hopefully nothing will go wrong :)
    os.rename(FILE_PATH, new_file_path)

    
    return True


if __name__ == "__main__":
    TVDB_API_KEY = tvdb.get_env_variable('TVDB_API_KEY')
    TVDV_ID = tvdb.get_env_variable('TVDV_ID')
    FILE_PATH = tvdb.get_env_variable('FILE_PATH')
    BEARER = tvdb.api_login(TVDB_API_KEY)

    rename_file_with_tvdb_id(BEARER, TVDV_ID, FILE_PATH)