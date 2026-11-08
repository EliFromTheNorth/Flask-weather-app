import requests


# Eget fel som visar att något gick fel vid hämtning av väderdata.
# Gör att routen bara behöver fånga ett fel och inte känna till requests.
class WeatherAPIError(Exception):
    pass


def fetch_weather(url):
    """Fetches weather data from api"""

    try:
        ### Tests:
        # answer = requests.get(url, timeout=(2, 0.00000000001))  #TEST - FEL: "Servern svarade inte i tid (Timeout)"
        # answer = requests.get("https://invalid-adress-12345", timeout=5)  #TEST - FEL: "Kunde inte nå servern. Kontrollera din internetanslutning."
        # answer = requests.get("https://httpbin.org/status/401", timeout=5)  #TEST - FEL: "HTTP-fel! Felkod: 401"
        # answer = requests.get("https://httpbin.org/html", timeout=5)  #TEST - FEL: "Ett fel uppstod vid hämtning av data." (ogiltig JSON)
        # answer = requests.get("https://invalid-adress-12345", timeout=5)  #TEST - FEL: "Ett fel uppstod vid hämtning av data."

        # timeout gör att appen inte hänger sig om API:et aldrig svarar
        answer = requests.get(url, timeout=5)
        answer.raise_for_status()  # Kontrollerar om servern svarade med ett HTTP-fel
        return answer.json()

    # Alla requests-fel görs om till vårt eget WeatherAPIError med ett läsbart meddelande.
    # Ordningen är viktig: de specifika felen först, det allmänna sist.
    except requests.Timeout as e:
        raise WeatherAPIError("The server did not respond in time (Timeout)") from e
    except requests.HTTPError as e:
        # Statuskoden hämtas ur svaret (om det finns) och visas för användaren
        status = e.response.status_code if e.response is not None else "unknown"
        raise WeatherAPIError(f"HTTP error! Status code: {status}") from e
    except requests.ConnectionError as e:
        raise WeatherAPIError(
            "Could not reach the server. Check your internet connection."
        ) from e
    # Fångar alla övriga requests-fel samt ogiltig JSON (ValueError)
    except (requests.RequestException, ValueError) as e:
        raise WeatherAPIError("An error occurred while fetching data.") from e
