from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
sys.path.insert(0, 'C:/Users/mdwil/PycharmProjects/TsunadeSenju') # Add current directory to the path
from creation_rebirth_sim import CreationRebirthModel # Import the original class
import numpy as np

app = Flask(__name__)
CORS(app)
