import os
import requests
import re
import traceback
import shutil


#
# TVDB DOCS: https://thetvdb.github.io/v4-api/
#

# Returns the bearer that is valid for 30 days
def api_login(TVDB_API_KEY):
    url = "https://api4.thetvdb.com/v4/login"
    response = requests.post(url, {}, { "apikey": TVDB_API_KEY },  headers={ 
        "accept": "application/json",
        "Content-Type": "application/json", 
    })
    
    if response.status_code != 200:
        raise SystemExit("ERROR unable to login!\n", response.text)
        return

    data = response.json()
    return data["data"]["token"]

def api_request(bearer, endpoint, params, data):
    url = "https://api4.thetvdb.com"+endpoint
    response = requests.get(url, params=params, data=data, headers={ 
        "accept": "application/json",
        "Content-Type": "application/json", 
        "Authorization": "Bearer "+bearer, 
    })

    if response.status_code != 200:
        print(f"ERROR {response.status_code} invalid api_request status code response for '{endpoint}' !\n", response.text)
    
    return response


def season_zerofill(number: int) -> str:
    if number < 10:
        return "0"+str(number)
    return str(number)


def episode_zerofill(number: int) -> str:
    if number < 10:
        return "000"+str(number)
    if number < 100:
        return "00"+str(number)
    if number < 1000:
        return "0"+str(number)
    return str(number)



def main(BEARER, MEDIA_PATH_FROM, MEDIA_PATH_TARGET):
    for filename in os.listdir(MEDIA_PATH_FROM):
        # construct full file path
        file_path = os.path.join(MEDIA_PATH_FROM, filename)
        
        # check if it is a file (and not a directory)
        if os.path.isfile(file_path):
            print(f"Processing file: {filename}")
        
            # regex for parsing series name and episode
            # group 1 = series name, group 1 = optional season number + episode number
            # IF group 2 contains "S" THEN it is correct 
            match = re.search(r'([a-zA-Z0-9!\.\?, ]*) - ([a-zA-Z0-9]*) +', file_path)

            # If a match is found, print the capture groups
            if match:
                series_name = match.group(1).strip()
                season_number = None
                episode_number = match.group(2).strip()
                print(f"Group 1 (series_name): {series_name}")
                print(f"Group 2 (episode_number): {episode_number}")

                if series_name.count == 0:
                    print("ERROR can not parse series_name out of file.")
                    continue
                if episode_number.count == 0:
                    print("ERROR can not parse episode_number out of file.")
                    continue

                # if first char in episode_number contains an 'S' then split it
                if episode_number[0] == "S":
                    ep_split = episode_number.split("E")
                    if len(ep_split) == 2:
                        season_number = ep_split[0]
                        episode_number = ep_split[1]
                    else:
                        print(f"ERROR can not split season+episode numbers from filename '{filename}'")
                        continue
                # episode_number should from here on be numeric
                if not episode_number.isnumeric():
                    print(f"ERROR episode_number '{episode_number}' should be numeric.")
                    continue

                # ​/episodes​/{id} to get seasonNumber and number
                try:
                    # GET: tvdb_id
                    response = api_request(BEARER, "/v4/search", { "query": series_name, "type": "series" }, {})
                    print(response.text)
                    response_data = response.json()

                    if response_data["status"] != "success" or len(response_data["data"]) == 0:
                        print(f"TVDB API found no match for series_name \"{series_name}\"")
                        continue
                    
                    # The TVDB search does not work always because of fucking live action series.
                    # Thats why we check results if they match series_name in a foreach and hope that the exact match is not a fucking live action series.
                    tvdb_id = None
                    for series in response_data["data"]:
                        if series["name"] == series_name or ("aliases" in series and series_name in series["aliases"]):
                            tvdb_id = series["tvdb_id"]
                            print(f"tvdb_id: {tvdb_id}")

                    if tvdb_id is None:
                        print(f"ERROR could not retrieve the tvdb_id from the data the API provided, because none of them matches the series name '{series_name}'.")
                        continue

                    # If the season+episode numbers are unkown then ask TVDB for it
                    if season_number is None:
                        # GET episode_id
                        response = api_request(BEARER, f"/v4/series/{tvdb_id}/episodes/absolute", { "page": 0, "season": 1, "episodeNumber": episode_number }, {})
                        # print(response.text)
                        response_data = response.json()
                        
                        try:
                            episode_id = response_data["data"]["episodes"][0]["id"]
                            print(f"episode_id: {episode_id}")
                        except Exception as e:
                            print("ERROR did not get episode_id out of TVDB")
                            continue

                        # GET seasonNumber, number (episode_number)
                        response = api_request(BEARER, f"/v4/episodes/{episode_id}", {}, {})
                        # print(response.text)
                        response_data = response.json()
                        
                        try:
                            season_number = response_data["data"]["seasonNumber"]
                            episode_number = response_data["data"]["number"]
                            print(f"season_number: {season_number}")
                            print(f"episode_number: {episode_number}")
                        except Exception as e:
                            print("ERROR did not get season_number or episode_number out of TVDB")
                            continue



                    season_number_str = season_zerofill(season_number)
                    episode_number_str = episode_zerofill(episode_number)
                    filename_split = filename.split(".")
                    filename_extention = filename_split[-1]
                    new_directory_path = f"{MEDIA_PATH_TARGET}/{series_name} {{tvdb-{tvdb_id}}}/Season {season_number_str}"
                    new_file_path = f"{new_directory_path}/{series_name} {{tvdb-{tvdb_id}}} - S{season_number_str}E{episode_number_str}.{filename_extention}"
                    print(f"new_file_path: {new_file_path}")

                    # Move the file finally and hopefully nothing will go wrong :)
                    os.makedirs(new_directory_path, exist_ok=True)
                    shutil.move(file_path, new_file_path)

                except Exception as e:
                    print(f"An error occurred: {e}")
                    print(traceback.format_exc())


def get_env_variable(name):
    value = os.getenv(name)
    if value is None:
        for i in range(3):
            print(f"The environment variable '{name}' was not set. Please make sure that all required environment variables mentioned in the README.md file are set. See: https://github.com/LuceusXylian/tvdb-season-episode-schema-rename")
        raise EnvironmentError(f"Environment variable '{name}' not found.")
    return value

if __name__ == "__main__":
    TVDB_API_KEY = get_env_variable('TVDB_API_KEY')
    MEDIA_PATH_FROM = get_env_variable('MEDIA_PATH_FROM')
    MEDIA_PATH_TARGET = get_env_variable('MEDIA_PATH_TARGET')
    BEARER = api_login(TVDB_API_KEY)
    main(BEARER, MEDIA_PATH_FROM, MEDIA_PATH_TARGET)
