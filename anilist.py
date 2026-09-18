import requests

def hent_data():
    query = """
    query ($page: Int){
      Page(page: $page, perPage: 50) {
        media(type: ANIME, sort: POPULARITY_DESC) {
          title { english romaji }
          genres
          averageScore
          popularity
          episodes
          coverImage { large }
        }
      }
    }
    """
    alle_anime = []

    for side in range(1, 11):
      response = requests.post(
          "https://graphql.anilist.co",
          json={
            "query": query,
            "variables": {"page": side}
          }
      )
      alle_anime += response.json()["data"]["Page"]["media"]

    return alle_anime

