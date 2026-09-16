import requests

def hent_data():
    query = """
    query {
      Page(page: 1, perPage: 100) {
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

    response = requests.post(
        "https://graphql.anilist.co",
        json={"query": query}
    )

    return response.json()

