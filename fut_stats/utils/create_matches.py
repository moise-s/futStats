# CREATE MATCHES ON DATABASE
import requests
import json
def send_post_requests_for_matches(matches, url):
    """
    Send a POST request to the specified URL for each match in the matches list.

    :param matches: List of match data to send as POST request data.
    :param url: URL to send the POST requests to.
    """
    for match in matches:
        try:
            response = requests.post(url, json=match)
            print(f"Sent POST request for match on {match['date']}. Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending request for match on {match['date']}: {e}")

# URL to send the POST requests to
url = "http://localhost:8000/match"

# Call the function with the list of matches and URL
json_file_path = 'fut_2023.json'

def load_matches_from_json(file_path):
    """
    Load matches data from a JSON file.

    :param file_path: Path to the JSON file.
    :return: List of matches loaded from the JSON file.
    """
    with open(file_path, 'r') as file:
        return json.load(file)
matches = load_matches_from_json(json_file_path)
send_post_requests_for_matches(matches, url)
