from src.gui import app
from flask import render_template, request
from src.common.handler import ParserHandler


@app.route('/')
@app.route('/index', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        search_string = request.form['search_input']
        domain_id = request.form['domain_input']
        # get result
        # render template
    elif request.method == 'GET':
        default_string = ""

    return render_template('index.html')
