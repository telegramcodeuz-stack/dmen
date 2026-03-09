from flask import Flask, render_template, request, jsonify, abort
import json
import os

app = Flask(__name__)

DB_FILE = "data/documents.json"

def load_docs():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

@app.route("/")
def index():
    return render_template("pin.html")

@app.route("/doc/<doc_id>")
def doc_page(doc_id):
    docs = load_docs()
    if doc_id not in docs:
        abort(404)
    return render_template("pin.html", doc_id=doc_id)

@app.route("/verify", methods=["POST"])
def verify():
    data = request.get_json()
    doc_id = data.get("doc_id")
    pin = data.get("pin")

    docs = load_docs()
    doc = docs.get(doc_id)

    if not doc:
        return jsonify({"ok": False, "error": "Hujjat topilmadi"})

    if doc.get("pin") != pin:
        return jsonify({"ok": False, "error": "PIN kod noto'g'ri"})

    return jsonify({"ok": True, "doc": doc["data"]})

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
