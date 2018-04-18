from flask import Flask

app = Flask(__name__)

from src.gui import routes
