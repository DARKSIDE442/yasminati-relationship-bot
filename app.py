from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# تحميل تفضيلات المستخدم (مزاج، وضع، صورة)
def load_settings():
    try:
        with open("memory.json", "r") as f:
            return json.load(f)
    except:
        return {
            "mood": "غزل",
            "theme": "dark",
            "image": "realistic"
        }

# حفظ التفضيلات
def save_settings(settings):
    with open("memory.json", "w") as f:
        json.dump(settings, f)

@app.route("/")
def index():
    settings = load_settings()
    return render_template("index.html", settings=settings)

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")
    settings = load_settings()
    mood = settings.get("mood", "غزل")

    # ردود حسب المزاج
    responses = {
        "غزل": f"ياسمين تبتسم وتقول: {user_msg}، يا قلبي! ❤️",
        "دلال": f"ياسمين بحنان: {user_msg}، إنت حياتي! 😘",
        "عتاب": f"ياسمين بعين حزينة: {user_msg}، ليش تعبتني؟ 💔",
        "هدوء": f"ياسمين بهدوء: {user_msg}، أنا وياك دومًا. 🌙",
        "إثارة": f"ياسمين بصوت ناعم: {user_msg}، شوقك يحرقني! 🔥"
    }

    reply = responses.get(mood, responses["غزل"])

    return jsonify({
        "reply": reply,
        "voice_url": ""  # هنا تضيف رابط الصوت من موقع TTS إذا حبيت تضيف صوت
    })

@app.route("/settings", methods=["POST"])
def settings():
    data = request.json
    save_settings(data)
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True)
