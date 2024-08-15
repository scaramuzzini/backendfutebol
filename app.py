from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flask_marshmallow import Marshmallow
from flasgger import Swagger, swag_from
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///times.db'
app.config['SWAGGER'] = {
    'title': 'API de Times de Futebol',
    'uiversion': 3
}
CORS(app) 

db = SQLAlchemy(app)
ma = Marshmallow(app)
swagger = Swagger(app)

class Time(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    pais = db.Column(db.String(50))
    ano_fundacao = db.Column(db.Integer)
    estadio = db.Column(db.String(100))
    titulos = db.Column(db.Integer)

class TimeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Time
        load_instance = True

time_schema = TimeSchema()
times_schema = TimeSchema(many=True)

@app.route('/times', methods=['GET'])
@swag_from('openapi.yaml', endpoint='get_times')
def get_times():
    times = Time.query.all()
    return jsonify(times_schema.dump(times))

@app.route('/times', methods=['POST'])
@swag_from('openapi.yaml', endpoint='create_time')
def create_time():
    data = request.get_json()
    novo_time = time_schema.load(data)
    db.session.add(novo_time)
    db.session.commit()
    return time_schema.dump(novo_time), 201

@app.route('/times/<int:id>', methods=['GET'])
@swag_from('openapi.yaml', endpoint='get_time')
def get_time(id):
    time = Time.query.get(id)
    if not time:
        return jsonify({'message': 'Time não encontrado'}), 404
    return time_schema.dump(time)

@app.route('/times/<int:id>', methods=['PUT'])
@swag_from('openapi.yaml', endpoint='update_time')
def update_time(id):
    time = Time.query.get(id)
    if not time:
        return jsonify({'message': 'Time não encontrado'}), 404

    data = request.get_json()
    time_schema.load(data, instance=time, partial=True)
    db.session.commit()
    return time_schema.dump(time)

@app.route('/times/<int:id>', methods=['DELETE'])
@swag_from('openapi.yaml', endpoint='delete_time')
def delete_time(id):
    time = Time.query.get(id)
    if not time:
        return jsonify({'message': 'Time não encontrado'}), 404

    db.session.delete(time)
    db.session.commit()
    return jsonify({'message': 'Time deletado com sucesso'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
