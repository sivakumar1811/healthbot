from flask import Flask, render_template, request
from chatbot import get_llm_response

app = Flask(__name__, static_folder='static')

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        user_input = request.form["symptoms"]
        result = get_llm_response(user_input)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
