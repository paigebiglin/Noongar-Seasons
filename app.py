from flask import Flask, jsonify, send_from_directory, request
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

@app.route('/season/<season_name>')
def season_page(season_name):
    with open('static/season.html') as f:
        html = f.read()
    html = html.replace('SEASON_PLACEHOLDER', season_name)
    return html

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

def load_signs():
    with open('data/signs.csv') as f:
        return list(csv.DictReader(f))

@app.route('/api/signs')
def get_signs():
    season = request.args.get('season')
    query = request.args.get('q')
    signs = load_signs()

    if season:
        signs = [s for s in signs if s['season_name'] == season]

    if query:
        query = query.lower()
        signs = [s for s in signs if query in s['name'].lower() or query in s['description'].lower()]

    return jsonify(signs)

@app.route('/search')
def search_page():
    query = request.args.get('q', '')
    with open('static/search.html') as f:
        html = f.read()
    html = html.replace('SEARCH_QUERY', '"' + query + '"' if query else 'null')
    return html

@app.route('/api/season-stats-ranked')
def get_season_stats_ranked():
    stats = get_season_stats().get_json()

    ranked = []
    for name, data in stats.items():
        entry = {'season_name': name}
        entry['avg_max_temp'] = data['avg_max_temp']
        entry['avg_min_temp'] = data['avg_min_temp']
        entry['total_rainfall'] = data['total_rainfall']
        entry['days_recorded'] = data['days_recorded']
        ranked.append(entry)

    for i in range(len(ranked)):
        for j in range(len(ranked) - 1 - i):
            if ranked[j]['total_rainfall'] < ranked[j + 1]['total_rainfall']:
                ranked[j], ranked[j + 1] = ranked[j + 1], ranked[j]

    return jsonify(ranked)

@app.route('/api/monthly-trend')
def get_monthly_trend():
    weather = load_weather()
    monthly = {}

    month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']

    for day in weather:
        month_key = day['date'][:7]
        if month_key not in monthly:
            monthly[month_key] = 0
        monthly[month_key] += float(day['rainfall_mm'])

    month_keys = list(monthly.keys())
    for i in range(len(month_keys)):
        for j in range(len(month_keys) - 1 - i):
            if month_keys[j] > month_keys[j + 1]:
                month_keys[j], month_keys[j + 1] = month_keys[j + 1], month_keys[j]

    trend = []
    for key in month_keys:
        year = key[:4]
        month_number = int(key[5:7])
        month_label = month_names[month_number - 1] + ' ' + year
        trend.append({'month': month_label, 'rainfall': round(monthly[key], 1)})

    return jsonify(trend)

@app.route('/analysis')
def analysis_page():
    return send_from_directory('static', 'analysis.html')

if __name__ == '__main__':
        app.run(debug=True, port=5001)