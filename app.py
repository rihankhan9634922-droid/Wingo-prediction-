from flask import Flask, jsonify
import random
import time
from datetime import datetime, timezone, timedelta

app = Flask(__name__)

# 10 AI Bots with English names, DP (avatars), and initial scores
BOTS_LIST = [
    {"id": 1, "name": "Sophia", "gender": "girl", "dp": "https://i.imgur.com/8Km9tLL.png", "score": 75},
    {"id": 2, "name": "Alexander", "gender": "boy", "dp": "https://i.imgur.com/2df4k9T.png", "score": 80},
    {"id": 3, "name": "Emma", "gender": "girl", "dp": "https://i.imgur.com/5g2x1LJ.png", "score": 70},
    {"id": 4, "name": "William", "gender": "boy", "dp": "https://i.imgur.com/9h7K4lQ.png", "score": 85},
    {"id": 5, "name": "Olivia", "gender": "girl", "dp": "https://i.imgur.com/4X1m8Zv.png", "score": 65},
    {"id": 6, "name": "James", "gender": "boy", "dp": "https://i.imgur.com/6y2p9Kt.png", "score": 90},
    {"id": 7, "name": "Ava", "gender": "girl", "dp": "https://i.imgur.com/3n8L2wR.png", "score": 72},
    {"id": 8, "name": "Benjamin", "gender": "boy", "dp": "https://i.imgur.com/7k4Q1mX.png", "score": 78},
    {"id": 9, "name": "Mia", "gender": "girl", "dp": "https://i.imgur.com/1p9K5vN.png", "score": 82},
    {"id": 10, "name": "Lucas", "gender": "boy", "dp": "https://i.imgur.com/8w3N6hL.png", "score": 88}
]

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Perfect Fit AI Predictor</title>
        <style>
            body { background-color: #121212; color: #ffffff; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; }
            .header { background: #1f1f1f; padding: 12px 15px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #333; position: sticky; top: 0; z-index: 100; }
            .mode-select { background: #2c2c2c; color: white; border: 1px solid #444; padding: 5px 10px; border-radius: 5px; font-weight: bold; }
            .refresh-btn { background-color: #0084ff; color: white; border: none; padding: 6px 12px; border-radius: 5px; cursor: pointer; font-weight: bold; }
            
            .game-board { background: #181818; padding: 15px; text-align: center; border-bottom: 1px solid #333; }
            .falling-box { font-size: 20px; font-weight: bold; animation: fall 0.5s ease-in-out; margin: 5px 0; }
            @keyframes fall { 0% { transform: translateY(-20px); opacity: 0; } 100% { transform: translateY(0); opacity: 1; } }
            
            .chat-container { padding: 10px; max-width: 600px; margin: auto; }
            .chat-card { background: #202c33; padding: 10px 12px; border-radius: 8px; margin-bottom: 10px; display: flex; align-items: center; box-shadow: 0 1px 3px rgba(0,0,0,0.3); }
            .dp { width: 45px; height: 45px; border-radius: 50%; object-fit: cover; margin-right: 12px; border: 1px solid #555; }
            .chat-info { flex-grow: 1; }
            .bot-name { font-weight: bold; font-size: 15px; color: #e9edef; }
            .score { font-size: 12px; color: #8696a0; margin-top: 2px; }
            .prediction-badge { padding: 5px 12px; border-radius: 6px; font-weight: bold; font-size: 13px; text-align: center; min-width: 60px; }
            .big { background:. #fa5858; color: white; background-color: #ff4757; }
            .small { background-color: #1e90ff; color: white; }
            .timer-box { font-size: 14px; color: #00ffcc; font-weight: bold; }
        </style>
    </head>
    <body>

        <div class="header">
            <div>
                <select id="gameMode" class="mode-select" onchange="updateMode()">
                    <option value="30s">30 Seconds</option>
                    <option value="1min">1 Minute</option>
                </select>
            </div>
            <div id="timer" class="timer-box">00:30</div>
            <button class="refresh-btn" onclick="fetchData()">Refresh</button>
        </div>

        <div class="game-board">
            <div style="font-size: 12px; color: #8696a0;" id="period-text">PERIOD: Loading...</div>
            <div id="fallingResult" class="falling-box" style="color: #00ffcc;">WAITING...</div>
        </div>

        <div class="chat-container" id="bots-container">
            <!-- Bots will load here -->
        </div>

        <script>
            let currentMode = '30s';

            function updateMode() {
                currentMode = document.getElementById('gameMode').value;
                fetchData();
            }

            function fetchData() {
                fetch('/api/data?mode=' + currentMode)
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('period-text').innerText = "PERIOD: " + data.period;
                        
                        let resDiv = document.getElementById('fallingResult');
                        resDiv.innerText = data.last_result;
                        resDiv.style.animation = 'none';
                        setTimeout(() => resDiv.style.animation = 'fall 0.5s ease-in-out', 10);

                        let container = document.getElementById('bots-container');
                        container.innerHTML = '';
                        
                        data.bots.forEach(bot => {
                            let predClass = bot.next === 'BIG' ? 'big' : 'small';
                            let card = `
                                <div class="chat-card">
                                    <img src="${bot.dp}" class="dp" alt="DP">
                                    <div class="chat-info">
                                        <div class="bot-name">${bot.name}</div>
                                        <div class="score">Accuracy / Score: ${bot.score}%</div>
                                    </div>
                                    <div class="prediction-badge ${predClass}">${bot.next}</div>
                                </div>
                            `;
                            container.innerHTML += card;
                        });
                    });
            }

            // Live Timer Synchronization
            function startTimer() {
                setInterval(() => {
                    let now = new Date();
                    let sec = now.getSeconds();
                    let timeLeft = currentMode === '30s' ? (sec < 30 ? 30 - sec : 60 - sec) : (60 - sec);
                    if (timeLeft === 60) timeLeft = 0;
                    document.getElementById('timer').innerText = "00:" + (timeLeft < 10 ? "0" : "") + timeLeft;
                    
                    if (timeLeft === 5) {
                        fetchData(); // Auto refresh near period change
                    }
                }, 1000);
            }

            fetchData();
            startTimer();
        </script>
    </body>
    </html>
    '''

@app.route('/api/data')
def get_data():
    from flask import request
    mode = request.args.get('mode', '30s')
    
    # Accurate live period calculation based on IST timezone
    ist_time = datetime.now(timezone(timedelta(hours=5, minutes=30)))
    total_seconds = ist_time.hour * 3600 + ist_time.minute * 60 + ist_time.second
    
    if mode == '30s':
        period_index = total_seconds // 30
    else:
        period_index = total_seconds // 60
        
    date_str = ist_time.strftime("%Y%m%d")
    period_number = f"{date_str}1000{1000 + period_index}"

    # Simulating dynamic score adjustments (+10% / -10% simulation logic)
    for bot in BOTS_LIST:
        change = random.choice([2, -2, 5, -5])
        bot['score'] = max(40, min(98, bot['score'] + change))
        bot['next'] = random.choice(["BIG", "SMALL"])

    last_result = f"{random.choice(['BIG', 'SMALL'])} ({random.randint(0, 9)})"

    return jsonify({
        "period": period_number,
        "last_result": last_result,
        "bots": BOTS_LIST
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090)
