from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)

# ====== Configuration ======
EMAIL = os.getenv("GDTOT_EMAIL", "YourEmail@gmail.com")
API_TOKEN = os.getenv("GDTOT_API_TOKEN", "CHANGE_ME")
DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"
TIMEOUT = float(os.getenv("HTTP_TIMEOUT", "25"))

API_LINK = "https://new.gdtot.com/api/upload/link"
API_FOLDER = "https://new.gdtot.com/api/upload/folder"


@app.route("/")
def home():
    return render_template("index.html")


def call_gdtot_api(url: str):
    if DEMO_MODE:
        # Sample payload similar to the one you posted
        sample = {
            "status": True,
            "code": 200,
            "message": "upload successful",
            "data": [
                {
                    "name": "File1.mkv",
                    "url": "https://new.gdtot.com/file/12345",
                    "size": "700.83 MB",
                    "id": "12345",
                    "mimeType": "video/x-matroska",
                    "message": "success",
                },
                {
                    "name": "File2.mkv",
                    "url": "https://new.gdtot.com/file/123456",
                    "size": "800.45 MB",
                    "id": "123456",
                    "mimeType": "video/x-matroska",
                    "message": "success",
                },
            ],
        }
        return sample

    payload = {
        "email": EMAIL,
        "api_token": API_TOKEN,
        "url": url,
    }
    endpoint = API_FOLDER if "folders" in url else API_LINK
    resp = requests.post(endpoint, data=payload, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


@app.route("/bypass", methods=["POST"])
def bypass():
    link = request.form.get("link", "").strip()
    if not link:
        return jsonify({"success": False, "error": "No link provided"}), 400

    try:
        data = call_gdtot_api(link)
        if data.get("status"):
            files = data.get("data", [])
            # normalize structure for frontend
            normalized = [
                {
                    "name": f.get("name") or "Unknown",
                    "url": f.get("url"),
                    "size": f.get("size", "?"),
                    "id": f.get("id"),
                    "mimeType": f.get("mimeType", ""),
                    "message": f.get("message", ""),
                }
                for f in files
                if f.get("url")
            ]
            return jsonify({"success": True, "files": normalized})
        return jsonify({"success": False, "error": data.get("message", "Unknown error")}), 400
    except requests.HTTPError as e:
        try:
            err_json = e.response.json()
            msg = err_json.get("message", str(e))
        except Exception:
            msg = str(e)
        return jsonify({"success": False, "error": msg}), 502
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    # For local testing only
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)
