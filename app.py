from flask import Flask, jsonify, request
from sklearn.externals import joblib
import sklearn

app = Flask(__name__)

@app.route("/")

def home():
  return 'La conexion es correcta'

if __name__ == '__main__':
    app.run()