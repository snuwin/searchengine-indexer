from flask import Flask, render_template, request, jsonify
import retrieve
import json

def webpagetourl(webpages):
    with open("WEBPAGES_RAW\\bookkeeping.json", "r") as file:
        data = json.load(file)
    return [data[x] for x in webpages]

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    if query:
        keys = retrieve.retrievesearch(query.split(" "))
        urls = webpagetourl([x[0] for x in keys])
        return render_template('results.html', query=query, urls=urls)
    else:
        return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)