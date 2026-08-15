from flask import Flask, jsonify
import random

app = Flask(__name__)

BOTS_LIST = [
    {"id": 1, "name": "Alpha Bot"},
    {"id": 2, "name": "Matrix AI"},
    {"id": 3, "name": "Nexus Pro"},
    {"id": 4, "name": "Vortex AI"},
    {"id": 5, "name": "Quantum X"},
    {"id": 6, "name": "Phoenix AI"},
    {"id": 7, "name": "Titan Bot"},
    {"id": 8, "name": "Cyber Win"},
    {"id": 9, "name": "Neural Predictor"},
    {"id": 10, "name": "Supreme AI"}
]

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Wingo AI Prediction</title>
        <style>
            body { background-color: #121212; color: #ffffff; font-family: Arial, sans-serif; margin: 0; padding: 10px; }
            .header { background: #1e1e1e; padding: 15px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
            .refresh-btn { background-color: #4CAF50; color: white; border: none; padding: 8px 12px; border-radius: 5px; cursor: pointer; font-weight: bold; }
            .bot-card { background: #1e1e1e; padding: 12px 15px; border-radius: 8px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }
            .bot-name { font-weight: bold; }
            .score { color: #4CAF50; font-size: 14px; }
            .prediction { background: #ff4444; color: white; padding: 5px 12px; border-radius: 5px; font-weight: bold; }
            .prediction.big { background: #ff4444; }
            .prediction.small { background: #2196F3; }
        </style>
    </head>
    <body>
        <div class="header">
            <div>
                <div style="font-size: 12px; color: #aaa;">PERIOD NUMBER</div>
                <div id="period" style="font-size: 16px; font-weight: bold;">Loading...</div>
            </div>
            <button class="refresh-btn" onclick="fetchData()">Refresh</button>
        </div>
        <h3 style="text-align: center; color: #ccc;">10 AI Bots Predictions</h3>
        <div id="bots-container"></div>
        <script>
            function fetchData() {
                fetch('/api/data')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('period').innerText = data.period;
                        let container = document.getElementById('bots-container');
                        container.innerHTML = '';
                        data.bots.forEach(bot => {
                            let predClass = bot.next === 'BIG' ? 'big' : 'small';
                            let card = `<div class="bot-card"><div><div class="bot-name">${bot.name}</div><div class="score">Score: ${bot.score}</div></div><div class="prediction ${predClass}">Next: ${bot.next}</div></div>`;
                            container.innerHTML += card;
                        });
                    });
            }
            fetchData();
            setInterval(fetchData, 5000);
        </script>
    </body>
    </html>
    '''

@app.route('/api/data')
def get_data():
    bots_data = []
    for bot in BOTS_LIST:
        score = random.randint(60, 95)
        prediction = random.choice(["BIG", "SMALL"])
        bots_data.append({
            "name": bot["name"],
            "score": f"{score}%",
            "next": prediction
        })
    
    current_period = "202608151000" + str(random.randint(1000, 9999))
    recent_result = random.choice(["BIG (9)", "SMALL (4)", "BIG (7)", "SMALL (2)"])

    return jsonify({
        "period": current_period,
        "result": recent_result,
        "bots": bots_data
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090)
