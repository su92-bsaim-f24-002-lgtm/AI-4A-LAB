from flask import Flask, render_template, request, jsonify
from weather_service import WeatherService

app = Flask(__name__)

THEMES = {
    "clear": {"primary": "#2196F3", "secondary": "#64B5F6", "text": "#333"},
    "clouds": {"primary": "#78909C", "secondary": "#B0BEC5", "text": "#333"},
    "rain": {"primary": "#1565C0", "secondary": "#1E88E5", "text": "#fff"},
    "snow": {"primary": "#ECEFF1", "secondary": "#CFD8DC", "text": "#333"},
    "thunderstorm": {"primary": "#4A148C", "secondary": "#7B1FA2", "text": "#fff"},
    "mist": {"primary": "#90A4AE", "secondary": "#B0BEC5", "text": "#333"},
    "default": {"primary": "#2196F3", "secondary": "#64B5F6", "text": "#333"},
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/weather", methods=["POST"])
def get_weather():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "No data provided"}), 400

    api_key = data.get("api_key", "").strip()
    city = data.get("city", "").strip()

    if not api_key:
        return jsonify({"success": False, "error": "API key is required"}), 400
    if not city:
        return jsonify({"success": False, "error": "City name is required"}), 400

    service = WeatherService(api_key)
    success, weather_data, error = service.get_weather(city)

    if success:
        formatted = WeatherService.format_weather_data(weather_data)
        theme = THEMES.get(formatted["condition"], THEMES["default"])
        return jsonify({"success": True, "data": formatted, "theme": theme})
    else:
        return jsonify({"success": False, "error": error})


@app.route("/api/theme/<condition>")
def get_theme(condition):
    theme = THEMES.get(condition, THEMES["default"])
    return jsonify(theme)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)