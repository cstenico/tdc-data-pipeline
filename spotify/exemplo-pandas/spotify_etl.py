import requests
from datetime import datetime
import datetime
import pandas as pd
import sqlalchemy
from sqlalchemy.orm import sessionmaker

DATABASE_LOCATION = "sqlite:///data/spotify.db"
TOKEN = "" # your Spotify API token

if __name__ == "__main__":
    
    #ETL?
    #Extract, Transform e Load

    #Extração


    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=TOKEN)
    }

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}&limit=50".format(time=yesterday_unix_timestamp), headers = headers)
    data = r.json()

    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []
    popularity_list = []

    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        popularity_list.append(song["track"]["popularity"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])

    song_dict = {
        "song_name" : song_names,
        "artist_name": artist_names,
        "popularity": popularity_list,
        "played_at" : played_at_list,
        "timestamp" : timestamps
    }

    #dataframe => estrutura de dado lidar com dados semi estruturados

    df_songs = pd.DataFrame(song_dict, columns = ["song_name", "artist_name", "popularity", "played_at", "timestamp"])

    #Transform
    if df_songs.empty:
        print("Não foi encontrado nenhum item")
        raise Exception("Nenhuma música foi encontrada")

    if pd.Series(df_songs['played_at']).is_unique:
        pass
    else:
        raise Exception("Mais de uma música executada ao mesmo tempo")

    if(pd.Series(df_songs["played_at"] < yesterday.isoformat() + 'Z').any()):
        raise Exception("Foram encontradas músicas executadas a mais de 24 horas")
    
    #ETL
    #Load

    engine = sqlalchemy.create_engine(DATABASE_LOCATION)

    try:
        df_songs.to_sql("played_tracks", engine, index=False, if_exists='append')
    except:
        print("Data already exists in the database")

    print("Close database successfully")


