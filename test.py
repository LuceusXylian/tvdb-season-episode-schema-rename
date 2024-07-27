import os
import main

TVDB_API_KEY = main.get_env_variable('TVDB_API_KEY')
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_PATH_FROM = SCRIPT_DIR+'/test/dl-completed'
MEDIA_PATH_TARGET = SCRIPT_DIR+'/test/series-files'


# Create some files to test with
def create_empty_file(filename):
    with open(filename, 'w') as file:
        pass

test_filenames = [
    "[SubsPlease] Wonderful Pretty Cure! - 24 (1080p) [BD05E4B4].mkv",
    "[SubsPlease] Boku no Hero Academia - 149 (1080p) [8543DF8E].mkv",
    "[SubsPlease] One Piece - 1111 (1080p) [DA084FD2].mkv",
]

for filename in test_filenames:
    create_empty_file(f"{MEDIA_PATH_FROM}/{filename}")


BEARER = main.api_login(TVDB_API_KEY)
main.main(BEARER, MEDIA_PATH_FROM, MEDIA_PATH_TARGET)