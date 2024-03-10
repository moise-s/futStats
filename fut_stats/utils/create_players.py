# CREATE PLAYERS
import requests
# The list of names to send in POST requests
names = [
    "Quint", "Eraldo", "Vini", "Duds", "Cava", "John", "Leo GK", "Rafa", "André GK",
    "Rayes GK", "Moises", "Vitinho Hasse", "Zé Love", "Murilo Joça GK", "Candemil",
    "Ota", "Felipe Rosa", "Schons", "Dani", "Daniel Schroder GK", "Igor", "Luis Martins (colega Duds)",
    "Martinez", "Tuco", "João Manke", "Pedro", "João JAPONEGO", "Otavio GK (colega Murilo)",
    "Lucas Augusto", "Vini (colega Zé Love)", "Marcelinho (colega Quint)", "Lui (colega Tuco)",
    "Vigorito", "Lessandro", "Itamar GK (pai do Moisés)", "Oppa", "Luiz Manke (irmão do João)",
    "Vitor Berreta (colega Rayes)", "Mauro Calói PR GK", "Biasi (colega Quint)", "Williams GK (aluguel)"
]

def send_post_requests(names, url):
    """
    Send a POST request to the specified URL for each name in the names list.

    :param names: List of names to send as POST request data.
    :param url: URL to send the POST requests to.
    """
    for name in names:
        try:
            response = requests.post(url, json={"name": name})
            print(f"Sent POST request for {name}. Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending request for {name}: {e}")

# URL to send the POST requests to
url = "http://localhost:8000/player"

# Call the function with the list of names and URL
send_post_requests(names, url)
