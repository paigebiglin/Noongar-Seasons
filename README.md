# Noongar Six Seasons

An interactive app exploring the Noongar six-season calendar, comparing traditional seasonal knowledge against real recorded weather data for Perth, WA.

**Live app:** https://paigebiglin.pythonanywhere.com

## Installation

1. Make sure Python 3 is installed.
2. Clone this repository:
```
git clone https://github.com/paigebiglin/Noongar-Seasons.git
cd Noongar-Seasons
```
3. Install Flask:
```
pip3 install flask
```

## Running the app
```
python3 app.py
```

Open `http://localhost:5001` in your browser.

## Using the app

- **Home page** — shows all six Noongar seasons, their traditional description, and their real recorded average temperature and total rainfall (calculated from Bureau of Meteorology data), plus a chart comparing total rainfall across all six seasons.
- **Season detail page** (click a season name) — shows all recorded environmental signs (animals, food sources, wildflowers, cultural practices) for that season, grouped by category, each with its source.
- **Search page** (link from the home page) — search all environmental signs by keyword across every season.

## Running the tests
```
python3 test_app.py
```

This runs 10 automated tests covering core functionality, the season-stats algorithm, filtering, and invalid input/edge cases.

## Data sources

- **Seasons and environmental signs** (`data/seasons.csv`, `data/signs.csv`): sourced from the Bureau of Meteorology's Nyoongar Calendar (bom.gov.au), Noongar Kaartdijin, WA Department of Fisheries, and DEECA Victoria (fire management). All entries are attributed by source in the data itself.
- **Weather data** (`data/weather.csv`): sourced from the Bureau of Meteorology's Daily Weather Observations for Perth (station 009225), August 2025 – July 2026, 364 daily records. Used under Creative Commons Attribution 4.0 International Licence. Manually transcribed from BOM's published PDF tables.

### Data cleaning

- December 9, 2025 was excluded from the weather dataset because BOM's source table was missing that day's maximum temperature reading. All other days in the 12-month period are complete.

## Algorithm

`app.py`'s `/api/season-stats` route maps each day in the weather dataset to its Noongar season (based on the month), then calculates the average maximum temperature, average minimum temperature, and total rainfall for each season. This allows direct comparison between what the traditional calendar describes and what was actually recorded.

## Architecture

Three-tier design: a browser frontend (HTML/JavaScript) calls a Flask backend (Python) via a JSON API, which reads from CSV data files. The browser never accesses the data files directly.

## AI assistance

This project was built with assistance from Claude (Anthropic), used to explain concepts, debug errors, and suggest code following patterns taught in CITS1501. All code was reviewed, tested, and understood before inclusion.
