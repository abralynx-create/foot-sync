import requests
import json
import time

# TA NOUVELLE CLÉ ACTIVE
API_KEY = '607e66b826eade008c396923680ed102'
BASE_URL = 'https://v3.football.api-sports.io/'

def get_live_matches_data():
    headers = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': 'v3.football.api-sports.io'}
    try:
        # On utilise une seule requête globale pour économiser tes 100 points
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
        <meta http-equiv="refresh" content="900">
        <title>Foot Sync - Live</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background-color: #050505; color: #fff; text-align: center; padding: 10px; margin: 0; }
            .header { background: #00ff00; color: #000; padding: 15px; font-weight: bold; font-size: 1.4em; border-bottom: 3px solid #fff; }
            .card { background: #151515; border-radius: 15px; padding: 15px; margin: 15px auto; max-width: 500px; border-bottom: 4px solid #00ff00; box-shadow: 0 4px 10px rgba(0,255,0,0.1); }
            .league { font-size: 0.75em; color: #00ff00; text-transform: uppercase; margin-bottom: 8px; font-weight: bold; }
            .time { color: #ff3e3e; font-weight: bold; font-size: 0.9em; margin-bottom: 10px; }
            .teams-row { display: flex; justify-content: space-between; align-items: center; margin: 10px 0; }
            .team { width: 35%; font-size: 1.1em; font-weight: bold; }
            .score { width: 30%; font-size: 2em; font-weight: bold; background: #252525; border-radius: 10px; color: #00ff00; padding: 5px 0; }
            .events-box { font-size: 0.85em; color: #ccc; border-top: 1px solid #333; margin-top: 15px; padding-top: 10px; text-align: left; line-height: 1.5; }
            .card-red { color: #ff3e3e; font-weight: bold; }
            .card-yellow { color: #ffd700; font-weight: bold; }
            .venue { font-size: 0.65em; color: #777; margin-top: 12px; font-style: italic; }
        </style>
    </head>
    <body>
        <div class="header">⚽ FOOT SYNC LIVE</div>
        <p style="font-size: 0.7em; color: #666;">MAJ AUTO 15 MIN • HEURE GMT : """ + time.strftime("%H:%M") + """</p>
    """
    
    if not live_matches:
        html_content += "<div style='margin-top:100px; color:#aaa;'>En attente de matchs en direct...<br>Le robot veille pour vous.</div>"
    else:
        for m in live_matches:
            events_list = []
            if 'events' in m and m['events']:
                for e in m['events']:
                    p = e['player']['name']
                    t = e['time']['elapsed']
                    extra = f"+{e['time']['extra']}" if e['time']['extra'] else ""
                    if e['type'] == 'Goal':
                        events_list.append(f"⚽ {p} ({t}{extra}')")
                    elif e['type'] == 'Card':
                        color_class = "card-red" if e['detail'] == 'Red Card' else "card-yellow"
                        icon = "🟥" if e['detail'] == 'Red Card' else "🟨"
                        events_list.append(f"<span class='{color_class}'>{icon} {p} ({t}{extra}')</span>")
            
            events_html = f'<div class="events-box">{"<br>".join(events_list)}</div>' if events_list else ""
            stade = m['fixture']['venue']['name'] or "Stade non précisé"
            temps = f"{m['fixture']['status']['elapsed']}"
            if m['fixture']['status']['extra']: temps += f"+{m['fixture']['status']['extra']}"

            html_content += f"""
            <div class="card">
                <div class="league">🏆 {m['league']['name']} ({m['league']['country']})</div>
                <div class="time">🔴 {temps}'</div>
                <div class="teams-row">
                    <div class="team">{m['teams']['home']['name']}</div>
                    <div class="score">{m['goals']['home']} - {m['goals']['away']}</div>
                    <div class="team">{m['teams']['away']['name']}</div>
                </div>
                {events_html}
                <div class="venue">📍 {stade}</div>
            </div>"""
            
    html_content += """
        <div style="margin-top:40px; padding: 20px; font-size:0.6em; color:#444;">
            Propulsé par Foot Sync Technology<br>Données en temps réel (Plan Free)
        </div>
    </body></html>"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    matches = get_live_matches_data()
    generate_html_page(matches)
