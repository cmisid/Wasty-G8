## --------------------------------------------------------
# Projet : WASTY
# Groupe 8 : Prediction et recommandation
# Objectif : Web service affichant le temps de disponibilite predit pour un objet   
## --------------------------------------------------------

from flask import Flask, jsonify
from available_time_prediction import available_time_prediction

app = Flask(__name__)

# On place les parametre dans l'URL
@app.route('/<buy_place>/<forecast_price>/<id_sub_category>/<object_state>/<quantite>/<situation>/<type_place>/<volume>/', methods=['GET'])
# Fonction retournant les probabilites au format json
def determine_object_price(buy_place,forecast_price,id_sub_category,object_state,quantite,situation,type_place,volume):

    u_req = [buy_place,forecast_price,id_sub_category,object_state,quantite,situation,type_place,volume,]
    res = available_time_prediction(u_req)

    payload = {
        'predicted_hour' : res
    }
    return jsonify(payload)

if __name__ == '__main__':
    app.run(debug=True)