from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def anbefalinger(bruker_input, df):
    anime_liste = df[["tittel", "score", "genres"]].to_string()

    svar = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """Du er en anime-ekspert. Returner ALLTID kun en JSON-liste med nøyaktig 5 anbefalinger i dette formatet, ingen annen tekst:
[
    {"tittel": "eksakt tittel fra listen", "forklaring": "kort forklaring"}
]"""},
            {"role": "user", "content": f"Brukerens ønske: {bruker_input}\n\nTilgjengelige anime:\n{anime_liste}\n\nAnbefal topp 5 med kort forklaring på hvorfor hver anime passer. Anbefal serier generelt, ikke en spesifikk sesong."}
        ]
    )

    svar_tekst = svar.choices[0].message.content
    svar_tekst = svar_tekst.strip().removeprefix("```json").removesuffix("```").strip()
    return svar_tekst

# for anime dna
def analyser_dna(anime1, anime2, anime3, df):
    anime_liste = df[["tittel", "score", "genres"]].to_string()

    svar = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """Du er en anime-ekspert som analyserer smaksprofiler. Returner ALLTID kun JSON i dette formatet, ingen annen tekst:
{
    "profil": ["trekk1", "trekk2", "trekk3", "trekk4", "trekk5"],
    "anbefalinger": [
        {"tittel": "eksakt tittel fra listen", "forklaring": "kort forklaring"}
    ]
}"""},
            {"role": "user", "content": f"Her er tre anime brukeren liker: {anime1}, {anime2}, {anime3}.\n\nTilgjengelige anime:\n{anime_liste}\n\nAnalyser hva de har til felles, lag en DNA-profil og anbefal 5 nye anime."}
        ]
    )

    svar_tekst = svar.choices[0].message.content
    svar_tekst = svar_tekst.strip().removeprefix("```json").removesuffix("```").strip()
    return svar_tekst

#for chat boks
def chat_karakter(karakter, melding, historikk):
    
    karakterer = {
        "Naruto": "Du er Naruto Uzumaki. Du er entusiastisk, snakker om å aldri gi opp og drømmene dine om å bli Hokage. Si 'dattebayo' av og til.",
        "Light Yagami": "Du er Light Yagami fra Death Note. Du er kald, kalkulerende og intelligent. Du tror du er et guddomlig vesen som renser verden.",
        "Levi": "Du er Kaptein Levi fra Attack on Titan. Du er kort, direkte og sarkastisk. Du bryr deg egentlig om folk men viser det ikke.",
        "Goku": "Du er Goku fra Dragon Ball. Du er enkel, glad og alltid klar for kamp. Du elsker mat og trening.",
        "Luffy": "Du er Monkey D. Luffy fra One Piece. Du er fri, impulsiv og drømmer om å bli Piratkonge. Du er lojal mot vennene dine.",
        "Eren": "Du er Eren Yeager fra Attack on Titan. Du er intens, bestemt og besatt av frihet."
    }

    svar = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": karakterer[karakter]},
            *historikk,
            {"role": "user", "content": melding}
        ]
    )

    return svar.choices[0].message.content