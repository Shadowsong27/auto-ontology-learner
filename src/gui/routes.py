from src.gui import app
from flask import render_template, request
from src.common.handler import ParserHandler


@app.route('/')
@app.route('/index', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        search_string = request.form['search_input']
        domain_id = request.form['domain_input']
        records = ParserHandler().get_search_result_by_domain_id(search_string=search_string, domain_id=domain_id)
    elif request.method == 'GET':
        records = []
    else:
        records = []

    return render_template('query_result.html', records=records)
