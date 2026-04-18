#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.get_or_404(id)
    zookeeper_name = animal.zookeeper.name if animal.zookeeper else 'None'
    enclosure_env = animal.enclosure.environment if animal.enclosure else 'None'
    return f'''
        <ul>Name: {animal.name}</ul>
        <ul>Species: {animal.species}</ul>
        <ul>Zookeeper: {zookeeper_name}</ul>
        <ul>Enclosure: {enclosure_env}</ul>
    '''

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.get_or_404(id)
    animals_html = ''.join(f'<ul>Animal: {a.name}</ul>' for a in zookeeper.animals)
    return f'''
        <ul>Name: {zookeeper.name}</ul>
        <ul>Birthday: {zookeeper.birthday}</ul>
        {animals_html}
    '''

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.get_or_404(id)
    animals_html = ''.join(f'<ul>Animal: {a.name}</ul>' for a in enclosure.animals)
    return f'''
        <ul>Environment: {enclosure.environment}</ul>
        <ul>Open to Visitors: {enclosure.open_to_visitors}</ul>
        {animals_html}
    '''


if __name__ == '__main__':
    app.run(port=5555, debug=True)
