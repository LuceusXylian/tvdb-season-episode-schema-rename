import requests

API_KEY = "1ee3f47d-69cf-4db7-a62f-3391c4683b59"

# Returns the bearer that is valid for 30 days
def api_login():
    url = "https://api4.thetvdb.com/v4/login"
    response = requests.post(url, {}, { "apikey": "1ee3f47d-69cf-4db7-a62f-3391c4683b59" },  headers={ 
        "accept": "application/json",
        "Content-Type": "application/json", 
    })
    
    if response.status_code != 200:
        print("ERROR unable to login!\n", response.text)
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
        print("ERROR unable to login!\n", response.text)
        return
    
    return response


def main():
    BEARER = api_login()

    # regex for parsing series name and episode
    # ([a-zA-Z0-9!\.\?, ]*) - ([a-zA-Z0-9]*) +
    # group 0 = series name, group 1 = episode number
    # IF group 1 contains "S" THEN it is correct 

    # ​/episodes​/{id} to get seasonNumber and number
    response = api_request(BEARER, "/v4/search", { "query": "E4596CED", "type": "series" }, {})
    print(response.json()["data"][0]["id"])
if __name__ == "__main__":
    main()
