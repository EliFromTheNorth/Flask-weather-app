import requests

def fetch_weather(url):
    """Fetches weather data from api"""

    try:
        ### Tests:
        # svar = requests.get(url, timeout=(2, 0.000000000000010)) #TEST - FEL: "Servern svarade inte i tid (Timeout)"
        # svar = requests.get(url, timeout=0.00000000005) #TEST - FEL: Kunde inte nå servern. Kontrollera din internetanslutning.
        # svar = requests.get("https://httpbin.org/status/401") #TEST - FEL: HTTP-fel! Felkod: {e.response.status_code}
        # svar = requests.get("https://httpbin.org/html") #TEST - FEL: Kunde inte tolka data från servern (ogiltig JSON).
        # svar = requests.get("invalid-adress-12345") #TEST - FEL: return "Ett nätverksfel uppstod vid hämtning av data."

        answer = requests.get(url, timeout=5)
        answer.raise_for_status()  # Kontrollerar om servern svarade med ett HTTP-fel
        return answer.json()

    except requests.Timeout as e:
        raise RuntimeError("Servern svarade inte i tid (Timeout)") from e
    except requests.HTTPError as e:
        status = e.response.status_code if e.response is not None
        raise RuntimeError(f"HTTP-fel! Felkod: {status}") from e
    except requests.ConnectionError as e:
        raise RuntimeError(
            "Kunde inte nå servern. Kontrollera din internetanslutning."
        ) from e
    except ValueError as e:
        raise RuntimeError("Kunde inte tolka data från servern (ogiltig JSON).") from e
    except requests.exceptions.RequestException as e:
        raise RuntimeError("Ett nätverksfel uppstod vid hämtning av data.") from e