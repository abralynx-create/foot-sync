import requests
import json
import time

# Ta configuration
API_KEY = 'b5e56855ed8f1cb06679af21683e0be5'
BASE_URL = 'https://v3.football.api-sports.io/'

def get_live_matches_data():
    headers = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': 'v3.football.api-sports.io'}
    try:
        # On demande les matchs en direct
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
        <title>Foot Sync - Live Scores</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0d0d0d; color: #fff; text-align: center; padding: 10px; margin: 0; }
            .header { background: #00ff00; color: #000; padding: 15px; font-weight: bold; font-size: 1.4em; letter-spacing: 2px; }
            .card { background: #1a1a1a; border-radius: 15px; padding: 15px; margin: 15px auto; max-width: 500px; border-left: 5px solid #00ff00; }
            .league { font-size: 0.75em; color: #00ff00; text-transform: uppercase; margin-bottom: 8px; font-weight: bold; }
            .live { color: #ff3e3e; font-weight: bold; animation: blink 1.2s infinite; font-size: 0.9em; }
            @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
            .teams-row { display: flex; justify-content: space-between; align-items: center; margin: 15px 0; }
            .team-name { width: 35%; font-size: 1.1em; font-weight: bold; }
            .score { width: 30%; font-size: 2em; font-weight: bold; color: #fff; }
            .events { font-size: 0.85em; color: #bbb; border-top: 1px solid #333; padding-top: 10px; text-align: left; }
            .venue { font-size: 0.7em; color: #666; font-style: italic; margin-top: 10px; }
        </style>
    </head>
    <body>
        <div class="header">FOOT SYNC LIVE</div>
        <p style="font-size: 0.8em; color: #888;">Dernière MAJ (GMT) : """ + time.strftime("%H:%M") + """</p>
    """
    
    if not live_matches:
        html_content += "<div style='margin-top:100px;'>En attente de matchs en direct...</div>"
    else:
        for m in live_matches:
            # Gestion des buteurs
            goal_events = []
            if 'events' in m and m['events']:
                for event in m['events']:
                    if event['type'] == 'Goal':
                        p = event['player']['name']
                        t = event['time']['elapsed']
                        goal_events.append(f"⚽ {p} ({t}')")
            
            events_html = ""
            if goal_events:
                events_html = '<div class="events">' + '<br>'.join(goal_events) + '</div>'

            # Gestion du stade
            stade = m['fixture']['venue']['name'] if m['fixture']['venue']['name'] else "Stade non renseigné"

            html_content += f"""
            <div class="card">
                <div class="league">🏆 {m['league']['name']} ({m['league']['country']})</div>
                <div class="live">🔴 {m['fixture']['status']['elapsed']}'</div>
                <div class="teams-row">
                    <div class="team-name">{m['teams']['home']['name']}</div>
                    <div class="score">{m['goals']['home']} - {m['goals']['away']}</div>
                    <div class="team-name">{m['teams']['away']['name']}</div>
                </div>
                {events_html}
                <div class="venue">📍 {stade}</div>
            </div>"""
            
    html_content += """
        <p style="margin-top:50px; font-size:0.6em; color:#333;">Design par Foot Sync</p>
    </body></html>
    """
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    matches = get_live_matches_data()
    generate_html_page(matches)
