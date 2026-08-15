import os
from flask import Flask, render_template_string
from datetime import datetime

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DARK SPECIAL - Live Server</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', sans-serif; }
        body { background-color: #f4f6f9; color: #333333; padding: 15px; max-width: 450px; margin: 0 auto; }
        .header { display: flex; justify-content: space-between; align-items: center; padding: 10px 0 20px 0; }
        .logo { font-size: 18px; font-weight: 800; letter-spacing: 2px; color: #007bff; }
        .top-info { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; font-size: 12px; font-weight: bold; color: #666666; letter-spacing: 1px; }
        .live-tag { background: #e1f5fe; color: #0288d1; padding: 4px 10px; border-radius: 12px; font-size: 10px; border: 1px solid #b3e5fc; }
        .prediction-card { background: #ffffff; border: 1px solid #e0e0e0; border-radius: 20px; padding: 25px 15px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
        .pred-title { color: #888888; font-size: 11px; letter-spacing: 2px; margin-bottom: 10px; }
        .main-prediction { font-size: 52px; font-weight: 900; color: #8e44ad; letter-spacing: 3px; margin: 5px 0; }
        .golden-title { color: #d35400; font-size: 10px; letter-spacing: 2px; margin-top: 15px; }
        .golden-numbers { font-size: 38px; font-weight: bold; color: #e67e22; margin: 5px 0; }
        .timer-section { margin: 20px 0 15px 0; }
        .timer-header { display: flex; justify-content: space-between; font-size: 11px; color: #666666; font-weight: bold; letter-spacing: 1px; margin-bottom: 8px; }
        .timer-clock { color: #007bff; font-size: 14px; font-family: monospace; font-weight: bold; }
        .progress-bar { width: 100%; height: 4px; background: #e0e0e0; border-radius: 2px; overflow: hidden; }
        .progress-fill { width: 100%; height: 100%; background: linear-gradient(90deg, #8e44ad, #007bff); transition: width 1s linear; }
        .stats-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-bottom: 20px; }
        .stat-card { background: #ffffff; border: 1px solid #e0e0e0; border-radius: 12px; padding: 12px 5px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.03); }
        .stat-label { font-size: 9px; color: #888888; letter-spacing: 1px; margin-bottom: 5px; }
        .stat-value { font-size: 20px; font-weight: bold; }
        .results-section { margin-bottom: 20px; }
        .results-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; margin-top: 10px; }
        .res-card { background: #ffffff; border: 1px solid #e0e0e0; border-radius: 10px; padding: 10px 0; text-align: center; box-shadow: 0 2px 6px rgba(0,0,0,0.03); }
        .res-num { font-size: 18px; font-weight: bold; color: #e67e22; }
        .res-type { font-size: 9px; color: #8e44ad; font-weight: bold; margin-top: 3px; }
    </style>
</head>
<body>
    <div class="header">
        <div style="font-size: 20px; cursor: pointer; color: #333;">☰</div>
        <div class="logo">DARK SPECIAL</div>
        <div style="font-size: 20px; color: #f39c12; cursor: pointer;">🔔</div>
    </div>

    <div class="top-info">
        <div>PERIOD: <span id="period-text" style="color: #111;">--</span></div>
        <div class="live-tag">● LIVE SERVER</div>
    </div>

    <div class="prediction-card">
        <div class="pred-title">NEXT PREDICTION</div>
        <div class="main-prediction" id="pred-text">SMALL</div>
        <div class="golden-title">★ GOLDEN NUMBERS</div>
        <div class="golden-numbers" id="golden-text">7 5</div>
    </div>

    <div class="timer-section">
        <div class="timer-header">
            <div>NEXT RESULT IN</div>
            <div class="timer-clock" id="timer-clock">00:30</div>
        </div>
        <div class="progress-bar">
            <div class="progress-fill" id="progress-fill"></div>
        </div>
    </div>

    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-label">ACCURACY</div>
            <div class="stat-value" style="color: #27ae60;">100.0%</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">WIN</div>
            <div class="stat-value" style="color: #27ae60;">7</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">LOSS</div>
            <div class="stat-value" style="color: #c0392b;">0</div>
        </div>
    </div>

    <div class="results-section">
        <div style="font-size: 11px; font-weight: bold; color: #666666; letter-spacing: 1px;">RECENT RESULTS</div>
        <div class="results-grid">
            <div class="res-card"><div class="res-num">2</div><div class="res-type">SMALL</div></div>
            <div class="res-card"><div class="res-num">7</div><div class="res-type" style="color: #007bff;">BIG</div></div>
            <div class="res-card"><div class="res-num">6</div><div class="res-type" style="color: #007bff;">BIG</div></div>
            <div class="res-card"><div class="res-num">9</div><div class="res-type" style="color: #007bff;">BIG</div></div>
            <div class="res-card"><div class="res-num">8</div><div class="res-type" style="color: #007bff;">BIG</div></div>
        </div>
    </div>

    <script>
        function updateTimer() {
            const now = new Date();
            const seconds = now.getSeconds();
            
            let remSeconds = 30 - (seconds % 30);
            if (remSeconds === 30) remSeconds = 0;

            const formattedSec = remSeconds < 10 ? '0' + remSeconds : remSeconds;
            document.getElementById('timer-clock').innerText = `00:${formattedSec}`;

            const progressPercent = (remSeconds / 30) * 100;
            document.getElementById('progress-fill').style.width = progressPercent + '%';

            const year = now.getFullYear();
            const month = String(now.getMonth() + 1).padStart(2, '0');
            const day = String(now.getDate()).padStart(2, '0');
            
            const totalMinutesToday = now.getHours() * 60 + now.getMinutes();
            const periodIntervals = totalMinutesToday * 2 + (seconds >= 30 ? 2 : 1);
            const periodNumberStr = `${year}${month}${day}1000${10000 + periodIntervals}`;
            
            document.getElementById('period-text').innerText = periodNumberStr;
        }

        setInterval(updateTimer, 100);
        updateTimer();
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
