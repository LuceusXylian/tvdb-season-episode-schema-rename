# Rename series media files to the season+episode schema

The goal of this python script is to move series from an input folder to the media/series folder and rename it to the S01E0001 schema.  
Also, before moving, the directories will be automatically created in the `{MEDIA_PATH_TARGET}/{series_name} {{tvdb-{tvdb_id}}}/Season {season_number}` schema.

An TVDB API key is required to make this script work. You can request one for free:
https://www.thetvdb.com/dashboard/account/apikey

## Environment variables
Before starting main.py please set the following ENV variables:
| Variable            | Description                              |
|---------------------|------------------------------------------|
| `TVDB_API_KEY`      | TVDB API key                             |
| `MEDIA_PATH_FROM`   | Input files directory                    |
| `MEDIA_PATH_TARGET` | The parent directory of all your series directories |



## Python requirements.txt
To update requirements.txt:
  pip freeze > requirements.txt

To install all libs from requirements.txt
  pip install -r requirements.txt