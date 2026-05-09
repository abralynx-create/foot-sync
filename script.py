import requests
import json
import time

# Ta configuration
API_KEY = 'b5e56855ed8f1cb06679af21683e0be5'
BASE_URL = 'https://v3.football.api-sports.io/'

def get_live_matches_data():
    headers = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': 'v3.football.api-sports.io'}
    try:
        response = requests.get(f"{BASE_URL}fixtures?live=all", headers=headers)
        return response.json().get('response', [])
    except:
        return []

def generate_html_page(live_matches):
    html_content = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="refresh" content="300">
        <title>Foot Sync - Scores en Direct</title>
        <style>
            body { font-family: sans-serif; background-color: #000; color: #fff; text-align: center; padding: 10px; }
            .card { background: #1a1a1a; border: 1px solid #333; border-radius: 8px; padding: 15px; margin: 10px auto; max-width: 400px; }
            .live { color: #00ff00; font-weight: bold; animation: blink 1s infinite; }
            @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
            .teams { font-size: 1.1em; margin: 10px 0; }
        </style>
    </head>
    <body>
        <h1 style="color:#00ff00;">⚽ Foot Sync Live</h1>
        <p>Mis à jour : """ + time.strftime("%H:%M") + """</p>
    """
    
    if not live_matches:
        html_content += "<p>Aucun match en direct pour le moment.</p>"
    else:
        for m in live_matches:
            html_content += f"""
            <div class="card">
                <div class="live">🔴 {m['fixture']['status']['elapsed']}'</div>
                <div class="teams">{m['teams']['home']['name']} {m['goals']['home']} - {m['goals']['away']} {m['teams']['away']['name']}</div>
                <div style="font-size:0.8em; color:#888;">{m['league']['name']}</div>
            </div>"""
            
    html_content += "</body></html>"
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    matches = get_live_matches_data()
    generate_html_page(matches)
