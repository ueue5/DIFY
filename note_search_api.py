from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


@app.route("/note_search", methods=["POST"])
def note_search():
    keyword = request.json.get("keyword")
    if not keyword:
        return jsonify({"error": "キーワードが必要です"}), 400

    search_url = "https://note.com/api/v3/searches"
    params = {"context": "note", "q": keyword, "size": 5, "start": 0}
    search_res = requests.get(search_url, params=params).json()

    articles = []

    for item in search_res["data"]["notes"]["contents"]:
        key = item.get("key")
        detail_url = f"https://note.com/api/v3/notes/{key}"
        detail_res = requests.get(detail_url).json()
        article_data = detail_res.get("data", {})
        articles.append({
            "title": article_data.get("name"),
            "url": f"https://note.com/{article_data.get('user', {}).get('urlname')}/{article_data.get('slug')}",
            "body": article_data.get("body", "")
        })

    return jsonify({"articles": articles})

if __name__ == "__main__":
    app.run(debug=True)
