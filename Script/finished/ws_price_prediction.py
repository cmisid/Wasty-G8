from flask import Flask, jsonify
from price_prediction import price_prediction

app = Flask(__name__)

# On place les parametre dans l'URL
@app.route('/<buy_place>/<id_sub_category>/<object_state>/<quantite>/<type_place>/<situation>/<volume>/', methods=['GET'])
# Fonction retournant les probabilites au format json
def determine_object_price(buy_place,id_sub_category,object_state,quantite,type_place,situation,volume):

    u_req = [buy_place,id_sub_category,object_state,quantite,type_place,situation,volume]
    inf,sup = price_prediction(u_req)

    payload = {
        'borne_inf' : inf,
        'borne_sup' : sup
    }
    return jsonify(payload)

if __name__ == '__main__':
    app.run(debug=True)
