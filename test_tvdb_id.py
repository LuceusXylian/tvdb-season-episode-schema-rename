import tvdb
import rename_with_tbdb_id
import test


if __name__ == "__main__":
    TVDB_API_KEY = tvdb.get_env_variable('TVDB_API_KEY')
    TVDV_ID = "81797"
    FILE_PATH = f"{test.MEDIA_PATH_FROM}/{test.test_filenames[0]}"
    BEARER = tvdb.api_login(TVDB_API_KEY)

    test.create_empty_file(FILE_PATH)

    rename_with_tbdb_id.rename_file_with_tvdb_id(BEARER, TVDV_ID, FILE_PATH)