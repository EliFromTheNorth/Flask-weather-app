# Väderapp

Flask-applikation som visar nuvarande väder och en prognos för tre dagar för fem svenska städer. Data hämtas från Open-Meteo API (CC BY 4.0): <https://open-meteo.com/>

## Kom igång

1. **Klona repot**

   ```bash
   git clone <repo-URL>
   cd <repo-mapp>
   ```

2. **Skapa och aktivera virtuell miljö**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # macOS / Linux / WSL
    venv\Scripts\activate # Windows (CMD / PowerShell)
    ```

3. **Installera beroenden**

    ```bash
    pip install -r requirements-dev.txt
    ```

4. **Kontroller före commit**

    *Linta koden:*
    ```bash
    ruff check .
    ```

    *Formatera koden:*
    ```bash
    ruff format .
    ```

    *Kör tester (inget nätverk behövs, alla API-anrop mockas):*
    ```bash
    pytest
    ```

5. **Starta applikationen:**

    ```bash
    flask run --debug
    ```
    Applikationen körs på: <http://127.0.0.1:5000/>

## Routar & filer

* `/` (HEM): Startsida med rullgardinslista över städerna
* `/<city_name>`: Prognossida med nuvarande väder och tabell för tre dagar
* `api.py`: alla anrop mot API:et (timeout, felhantering, eget fel `WeatherAPIError`)
* `weather_service.py`: hanterar stadslistan och bygger tabellerna
* `tests/`: tester med Pytest

## Frågor

**1. Varför mockar du anropen mot API:et i dina tester, och vad skulle hända om du inte gjorde det?**

Jag mockar anropen för att kunna testa att mina funktioner ger rätt resultat utan att hämta data på riktigt. Testerna behöver då ingen internetanslutning. Utan mockning skulle ett nätverksfel få testet att misslyckas fast koden är rätt skriven, och jag skulle inte kunna framkalla fel som timeout och HTTP-fel när jag vill.

**2. Vad gör timeout och raise_for_status(), och varför behövs de?**

`timeout=5` gör att anropet avbryts efter 5 sekunder om API:et inte svarar, så att appen inte hänger sig. 
`raise_for_status()` kastar ett HTTPError om servern svarar med en felkod (4xx eller 5xx), annars skulle felsvaret behandlas som vanlig data. Jag gör om felen till mitt eget `WeatherAPIError`, så att användaren får ett felmeddelande och appen inte kraschar.

**3. Hur fungerar mallarv i Jinja2?**

Grundstrukturen skriver jag en gång i `base.html`, med navigering, footer och ett block `content`. De andra mallarna börjar med `{% extends "base.html" %}` och fyller bara i blocket. Då slipper jag upprepa samma HTML på varje sida.

**4. Vad är en fixture, och vilken använder du?**

En fixture är en funktion som förbereder något som flera tester behöver. Jag använder fixturen `client`, som ger Flasks testklient, så att jag kan anropa mina routes utan att starta appen.