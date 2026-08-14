from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

TOKEN = "ws_64febebc8e74a5154ebb1d72a30ea4397265d56772b0ec5119b160d7286b0182"

game_endpoints = {
    "30sec": "30-sec-game-history",
    "1min": "1-min-game-history",
    "3min": "3-min-game-history",
    "5min": "5-min-game-history"
}

game_data = {
    "30sec": {"period": "Loading...", "number": "-", "result": "-", "color": "gray", "timer": 30},
    "1min": {"period": "Loading...", "number": "-", "result": "-", "color": "gray", "timer": 60},
    "3min": {"period": "Loading...", "number": "-", "result": "-", "color": "gray", "timer": 180},
    "5min": {"period": "Loading...", "number": "-", "result": "-", "color": "gray", "timer": 300}
}

bots = [
    "Alpha Bot", "Matrix AI", "Nexus Pro", "Vortex AI", "Quantum X",
    "Phoenix AI", "Titan Bot", "Cyber Win", "Pulse AI", "Apex Master"
]

scores = {g: {name: 75 for name in bots} for g in game_endpoints}
bet_history = {g: {name: ["BIG", "SMALL", "BIG", "SMALL", "BIG", "SMALL", "BIG", "SMALL", "BIG", "SMALL"] for name in bots} for g in game_endpoints}
next_predictions = {g: {name: "BIG" for name in bots} for g in game_endpoints}

html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Daman AI Predictor</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background-color: #121212; color: #e0e0e0; font-family: Arial, sans-serif; margin: 0; padding: 0; }
        .header { background: linear-gradient(135deg, #1f1f1f, #2d2d2d); color: #ff4d4d; padding: 15px; text-align: center; font-size: 20px; font-weight: bold; border-bottom: 2px solid #333; }
        .tabs { display: flex; justify-content: space-around; background: #1e1e1e; padding: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.5); }
        .tab { padding: 8px 10px; background: #2c2c2c; border-radius: 8px; font-size: 11px; font-weight: bold; color: #aaa; text-decoration: none; cursor: pointer; }
        .tab.active { background: #ff4d4d; color: white; }
        .card { background: #1e1e1e; margin: 15px; padding: 15px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); border: 1px solid #2c2c2c; }
        .flex-box { display: flex; justify-content: space-between; align-items: center; }
        .bot-card { background: #252525; border: 1px solid #333; border-radius: 8px; margin-bottom: 10px; overflow: hidden; }
        .bot-header { display: flex; justify-content: space-between; font-weight: bold; font-size: 14px; align-items: center; color: #fff; padding: 12px; cursor: pointer; background: #2a2a2a; }
        .bot-header:active { background: #333; }
        .next-pred { font-size: 12px; padding: 3px 8px; border-radius: 5px; color: white; font-weight: bold; }
        .pred-big { background-color: #ff4d4d; }
        .pred-small { background-color: #2196F3; }
        .bot-details { display: none; padding: 12px; border-top: 1px solid #333; background: #1e1e1e; }
        .history-box { display: flex; gap: 5px; overflow-x: auto; margin-top: 8px; padding-top: 5px; }
        .badge { font-size: 10px; padding: 4px 6px; border-radius: 4px; font-weight: bold; color: white; text-align: center; min-width: 35px; }
        .badge-big { background-color: #ff4d4d; }
        .badge-small { background-color: #2196F3; }
        .color-dot { display: inline-block; width: 12px; height: 12px; border-radius: 50%; margin-right: 5px; }
        .green { background-color: #4CAF50; }
        .red { background-color: #f44336; }
        .violet { background-color: #9c27b0; }
    </style>
    <script>
        let timeLeft = __TIMER_SECS__;
        function startTimer() {
            setInterval(function() {
                if (timeLeft > 0) {
                    timeLeft--;
                } else {
                    timeLeft = __MAX_TIME__;
                    location.reload();
                }
                let mins = Math.floor(timeLeft / 60);
                let secs = timeLeft % 60;
                let timeStr = (mins < 10 ? "0" : "") + mins + ":" + (secs < 10 ? "0" : "") + secs;
                let timerEl = document.getElementById("timer-display");
                if(timerEl) timerEl.innerText = timeStr;
            }, 1000);
        }
        function toggleBot(id) {
            let box = document.getElementById(id);
            if (box.style.display === "block") {
                box.style.display = "none";
            } else {
                box.style.display = "block";
            }
        }
        window.onload = startTimer;
    </script>
</head>
<body>
    <div class="header">Daman AI Predictor</div>
    <div class="tabs">
        <a href="/?game=30sec" class="tab __TAB_30SEC__">WinGo 30sec</a>
        <a href="/?game=1min" class="tab __TAB_1MIN__">WinGo 1 Min</a>
        <a href="/?game=3min" class="tab __TAB_3MIN__">WinGo 3 Min</a>
        <a href="/?game=5min" class="tab __TAB_5MIN__">WinGo 5 Min</a>
    </div>
    <div class="card">
        <div class="flex-box">
            <div>
                <div style="font-size: 11px; color: #888;">PERIOD NUMBER</div>
                <div style="font-weight: bold; font-size: 12px; color: #fff;">__PERIOD__</div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 11px; color: #888;">TIMER & RESULT</div>
                <div style="font-weight: bold; font-size: 14px; color: #fff;">
                    <span id="timer-display" style="color: #ff4d4d; margin-right: 8px;">__TIMER__</span>
                    <span class="color-dot __COLOR_CLASS__"></span>__RESULT__ (__NUMBER__)
                </div>
            </div>
        </div>
    </div>
    <div class="card">
        <h3 style="margin-top: 0; font-size: 15px; color: #fff;">10 AI Bots (Click to Open Bets)</h3>
        __BOT_CARDS__
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    current_game = request.args.get("game", "30sec")
    if current_game not in game_endpoints:
        current_game = "30sec"

    endpoint = game_endpoints[current_game]
    try:
        r = requests.get(f"https://api.wingobot.com/v2/{endpoint}", headers={"Authorization": f"Bearer {TOKEN}"}, timeout=3)
        data = r.json()
        if data.get("success"):
            current = data["current"]
            history = data["history"][0]
            game_data[current_game]["period"] = current["issueNumber"]
            num = int(history["number"])
            game_data[current_game]["number"] = num
            game_data[current_game]["result"] = "BIG" if num >= 5 else "SMALL"
            game_data[current_game]["color"] = history["colour"].lower()
    except:
        pass

    bot_cards_html = ""
    g_scores = scores[current_game]
    g_history = bet_history[current_game]
    g_next = next_predictions[current_game]
    sorted_bots = sorted(g_scores.items(), key=lambda x: x[1], reverse=True)

    for idx, (name, score) in enumerate(sorted_bots):
        next_bet = g_next[name]
        pred_class = "pred-big" if next_bet == "BIG" else "pred-small"
        
        history_badges = ""
        for bet in g_history[name]:
            if bet == "BIG":
                history_badges += "<span class='badge badge-big'>BIG</span>"
            else:
                history_badges += "<span class='badge badge-small'>SMALL</span>"
        
        bot_id = f"bot_details_{idx}"
        bot_cards_html += f"""
        <div class="bot-card">
            <div class="bot-header" onclick="toggleBot('{bot_id}')">
                <div>
                    <span>💬 {name}</span><br>
                    <span style="font-size: 11px; color: #4CAF50; font-weight: normal;">Score: {score}% (Tap to view bets)</span>
                </div>
                <div>
                    <span style="font-size: 10px; color: #888;">Next: </span>
                    <span class="next-pred {pred_class}">{next_bet}</span>
                </div>
            </div>
            <div id="{bot_id}" class="bot-details">
                <div style="font-size: 11px; color: #aaa; margin-bottom: 5px;">Bot's Last 10 Bets History:</div>
                <div class="history-box">
                    {history_badges}
                </div>
            </div>
        </div>
        """

    info = game_data[current_game]
    page = html_template.replace("__PERIOD__", str(info["period"]))
    page = page.replace("__RESULT__", str(info["result"]))
    page = page.replace("__NUMBER__", str(info["number"]))
    
    secs = info["timer"]
    max_t = 30 if current_game == "30sec" else (60 if current_game == "1min" else (180 if current_game == "3min" else 300))
    
    page = page.replace("__TIMER_SECS__", str(secs))
    page = page.replace("__MAX_TIME__", str(max_t))
    
    mins = secs // 60
    rem_secs = secs % 60
    time_str = f"{mins:02d}:{rem_secs:02d}"
    page = page.replace("__TIMER__", time_str)
    
    c_class = "green"
    if "red" in info["color"]:
        c_class = "red"
    elif "violet" in info["color"]:
        c_class = "violet"
    page = page.replace("__COLOR_CLASS__", c_class)
    
    page = page.replace("__TAB_30SEC__", "active" if current_game == "30sec" else "")
    page = page.replace("__TAB_1MIN__", "active" if current_game == "1min" else "")
    page = page.replace("__TAB_3MIN__", "active" if current_game == "3min" else "")
    page = page.replace("__TAB_5MIN__", "active" if current_game == "5min" else "")
    
    page = page.replace("__BOT_CARDS__", bot_cards_html)
    return page

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090￼Enter
