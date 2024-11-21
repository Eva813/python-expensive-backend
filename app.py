from flask import Flask, jsonify, request
import expensive_mongo as em
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/items/', methods=['GET'])
def get_items():
    return jsonify(em.get_items())


@app.route('/item/', methods=['POST'])
def add_item():
    data = request.get_json()
    print(data)
    if em.add_item(data['name'], data['price'], data['type']):
        result = jsonify(message='add item successful')
    else:
        result = jsonify(message='add item failed')
    return result


@app.route('/item/<obj_id>', methods=['DELETE'])
def delete_item(obj_id):
    if em.remove_item(obj_id):
        result = jsonify(message='delete item successful')
    else:
        result = jsonify(message='delete item failed')
    return result


if __name__ == '__main__':
    app.run(debug=True)

