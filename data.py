import pandas as pd
from anilist import hent_data

#hente data fra api
data =  hent_data()
rader = []
for anime in data["data"]["Page"]["media"]:
    rader.append({
        'tittel': anime["title"]["english"] or anime["title"]["romaji"],
        'score' : anime["averageScore"],
        'genres' : ",".join(anime["genres"]),
        'bilde' : anime["coverImage"]["large"]

    }
    )
df = pd.DataFrame(rader)
