from flask import Flask, render_template, jsonify
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
    return render_template('index.html')

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
    app.run(host="0.0.0.0", port=8090)￼Enter
