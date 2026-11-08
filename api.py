import requests

def fetch_weather(url):
    """Fetches weather data from api"""

    try:
        ### Tests:
        # answer = requests.get(url, timeout=(2, 0.00000000001))  #TEST - FEL: "Servern svarade inte i tid (Timeout)"
        # answer = requests.get("https://invalid-adress-12345", timeout=5)  #TEST - FEL: "Kunde inte nå servern. Kontrollera din internetanslutning."
        # answer = requests.get("https://httpbin.org/status/401", timeout=5)  #TEST - FEL: "HTTP-fel! Felkod: 401"
        # answer = requests.get("https://httpbin.org/html", timeout=5)  #TEST - FEL: "Ett fel uppstod vid hämtning av data." (ogiltig JSON)
        # answer = requests.get("https://invalid-adress-12345", timeout=5)  #TEST - FEL: "Ett fel uppstod vid hämtning av data."

        answer = requests.get(url, timeout=5)
        answer.raise_for_status()  # Kontrollerar om servern svarade med ett HTTP-fel
        return answer.json()

    except requests.Timeout as e:
        raise RuntimeError("The server did not respond in time (Timeout)") from e
    except requests.HTTPError as e:
        status = e.response.status_code if e.response is not None else "unknown"
        raise RuntimeError(f"HTTP error! Status code: {status}") from e
    except requests.ConnectionError as e:
        raise RuntimeError(
            "Could not reach the server. Check your internet connection."
        ) from e
    except (requests.RequestException, ValueError) as e:
        raise RuntimeError("An error occurred while fetching data.") from e