from flask import Flask, render_template, request
from flask import jsonify
import databaza

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pumpy/<nazov>')
def pumpy_pri_ceste(nazov):
    return jsonify(databaza.pumpy_pri_ceste(nazov))

@app.route('/pumpy')
def pumpy_pri_bode():
    sirka = request.args.get('lat')
    dlzka = request.args.get('lng')
    return jsonify(databaza.pumpy_pri_bode(sirka,dlzka))

@app.route('/mesto/<nazov>')
def pumpy_v_meste(nazov):
    return jsonify(databaza.pumpy_v_oblasti(nazov))

if __name__ == '__main__':
    app.run()
