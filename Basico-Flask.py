from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Configuración de la base de datos
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/test'  # Base de datos en localhost
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definición del modelo
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# Crear las tablas si no existen
with app.app_context():
    db.create_all()

# Clase básica de Endpoints
class BasicAPI:
    @app.route('/items', methods=['GET'])
    def get_all_items():
        items = Item.query.all()
        return jsonify([{'id': item.id, 'name': item.name} for item in items])

    @app.route('/items/<int:item_id>', methods=['GET'])
    def get_item(item_id):
        item = Item.query.get_or_404(item_id)
        return jsonify({'id': item.id, 'name': item.name})

    @app.route('/items', methods=['POST'])
    def create_item():
        data = request.get_json()
        new_item = Item(name=data['name'])
        db.session.add(new_item)
        db.session.commit()
        return jsonify({'id': new_item.id, 'name': new_item.name}), 201

    @app.route('/items/<int:item_id>', methods=['DELETE'])
    def delete_item(item_id):
        item = Item.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted'}), 200

# Instanciar la clase para registrar los endpoints
api = BasicAPI()

if __name__ == '__main__':
    app.run(debug=True)
