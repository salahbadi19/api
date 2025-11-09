from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)

# تفعيل CORS للأصل المحدد فقط
CORS(app, resources={r"/*": {"origins": "https://qxbroker-api-v3.web.app"}})

# الحالة الحالية والأعدادات
RUNNING = False
SELECTED_ASSETS = []
DURATION = 10

# مفتاح سري للتحقق من الطلبات (من الأداة أو الموقع)
API_SECRET = os.environ.get("API_SECRET", "change_this_secret")

# دالة للتحقق من المفتاح السري
def verify_api_key(req):
    key = req.headers.get("X-API-KEY")
    return key == API_SECRET

# Endpoint لتشغيل الأداة
@app.route("/start", methods=["POST"])
def start_tool():
    global RUNNING
    if not verify_api_key(request):
        return jsonify({"error": "unauthorized"}), 401
    RUNNING = True
    return jsonify({"status": "started"})

# Endpoint لإيقاف الأداة
@app.route("/stop", methods=["POST"])
def stop_tool():
    global RUNNING
    if not verify_api_key(request):
        return jsonify({"error": "unauthorized"}), 401
    RUNNING = False
    return jsonify({"status": "stopped"})

# Endpoint لتحديث الإعدادات
@app.route("/settings", methods=["POST"])
def update_settings():
    global SELECTED_ASSETS, DURATION
    if not verify_api_key(request):
        return jsonify({"error": "unauthorized"}), 401

    data = request.json
    assets = data.get("assets")
    duration = data.get("duration", 10)

    if not assets:
        return jsonify({"error": "No assets provided"}), 400

    SELECTED_ASSETS = assets
    DURATION = int(duration)

    return jsonify({
        "status": "settings updated",
        "assets": SELECTED_ASSETS,
        "duration": DURATION
    })

# Endpoint لجلب حالة الأداة والإعدادات
@app.route("/status", methods=["GET"])
def status():
    if not verify_api_key(request):
        return jsonify({"error": "unauthorized"}), 401
    return jsonify({
        "running": RUNNING,
        "assets": SELECTED_ASSETS,
        "duration": DURATION
    })

# Endpoint افتراضي لجلب بيانات الشموع (مثال)
@app.route("/candles", methods=["GET"])
def candles():
    if not verify_api_key(request):
        return jsonify({"error": "unauthorized"}), 401
    if not RUNNING:
        return jsonify({"error": "API is stopped"}), 400

    # مثال بيانات وهمية — استبدلها لاحقًا ببيانات الأداة
    data = {}
    for asset in SELECTED_ASSETS:
        data[asset] = [
            {"buy": 50, "sell": 50},
            {"buy": 52, "sell": 48},
            {"buy": 49, "sell": 51},
        ][:DURATION]
    return jsonify(data)

if __name__ == "__main__":
    # شغل API على Render
    app.run(host="0.0.0.0", port=8000)
