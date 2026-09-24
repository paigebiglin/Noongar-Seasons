from flask import Flask, jsonify, send_from_directory
import csv

app = Flask(__name__, static_folder='static')

def load_seasons():
    with open('data/seasons.csv') as f:
        return list(csv.DictReader(f))

@app.route('/')
def home():
        return send_from_directory('static', 'index.html')

@app.route('/api/seasons')
def get_seasons():
        return jsonify(load_seasons())

def load_weather():
    with open('data/weather.csv') as f:
        return list(csv.DictReader(f))

def date_to_season(date_str):
    month = int(date_str.split('-')[1])
    if month in [12, 1]:
        return 'Birak'
    elif month in [2, 3]:
        return 'Bunuru'
    elif month in [4, 5]:
        return 'Djeran'
    elif month in [6, 7]:
        return 'Makuru'
    elif month in [8, 9]:
        return 'Djilba'
    elif month in [10, 11]:
        return 'Kambarang'
    return None

@app.route('/api/season-stats')
def get_season_stats():
    weather = load_weather()
    totals = {}

    for day in weather:
        season = date_to_season(day['date'])
        if season is None:
            continue

        if season not in totals:
            totals[season] = {'max_sum': 0, 'min_sum': 0, 'rain_sum': 0, 'count': 0}

        totals[season]['max_sum'] += float(day['max_temp'])
        totals[season]['min_sum'] += float(day['min_temp'])
        totals[season]['rain_sum'] += float(day['rainfall_mm'])
        totals[season]['count'] += 1

    stats = {}
    for season, t in totals.items():
        if t['count'] == 0:
            continue
        stats[season] = {
            'avg_max_temp': round(t['max_sum'] / t['count'], 1),
            'avg_min_temp': round(t['min_sum'] / t['count'], 1),
            'total_rainfall': round(t['rain_sum'], 1),
            'days_recorded': t['count']
        }

    return jsonify(stats)

if __name__ == '__main__':
        app.run(debug=True, port=5001)