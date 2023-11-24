from dotenv import load_dotenv
import os
import base64
from requests import post, get  
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


class Spotify:

    _token: str
    url: str

    def __init__(self) -> None:

        self._token = self.__get_token()

        pass

    def get_auth_header(self):
        return {"Authorization": "Bearer "+self._token }

    def __get_token(self):
        auth_string = client_id+":"+client_secret
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic "+auth_base64,
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {"grant_type": "client_credentials"}

        result = post(url, headers=headers, data=data)
        json_result = json.loads(result.content)
        return  json_result["access_token"]


    def create_playlist(self, token, name: str, tracks_ids:list):
        url =  "https://api.spotify.com/v1/users/lp.109lm-gt/playlists"
        payload = {
                "name": name,
            }
        result_cr_playlist = post(
            url=url,
            data=json.dumps(payload), 
            headers={
                "Authorization": "Bearer "+token
            }
        )
        create_playlist_return =  json.loads(result_cr_playlist.content)

        if "error" in create_playlist_return:
            return create_playlist_return
        

        playlist_id = create_playlist_return["id"]
        url =  f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        payload = {
            "uris": [f"spotify:track:{track_id}" for track_id in tracks_ids],
            "position": 0
        }

        result_add_tracks = post(
            url=url,
            data=json.dumps(payload), 
            headers={
                "Authorization": "Bearer "+token
            }
        )
    
        if "error" in result_add_tracks:
            return result_add_tracks
        
        return 


def main():
    spotify: Spotify = Spotify()
    token = "BQClRGumgLWvYka4hil82TYoscxbTSLRvAdGOXK17nvchgJB9Pk3p8evNdasv7gybZ9-phzX17UcDcwriTjyurnhuoEJye6fs6jjU-StoahBl_7P715zsH_5vnv6pBrXn2ZsZiE08HZSdayqUdGC-BdaJlf5Xt22MBwQ5Yf6lye-3QiOPH1G3wYn7RdqhW50NEYK-8oL2mR3e3Imi_pNFjOTTYlYfc5jXnYVzvpQsGkmHVqX94dcACYHGE_QBQ"
    print(spotify.create_playlist(token, "hey yo", []))


if __name__ == "__main__":
    main()