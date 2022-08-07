from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Library, library_schema, libraries_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/libraries', methods = ['POST'])
@token_required
def create_library(current_user_token):
    author_name = request.json['author_name']
    book_title = request.json['book_title']
    ISBN_number = request.json['ISBN_number']
    book_length = request.json['book_length']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    library = Library(author_name, book_title, ISBN_number, book_length, user_token = user_token )

    db.session.add(library)
    db.session.commit()

    response = library_schema.dump(library)
    return jsonify(response)

@api.route('/libraries', methods = ['GET'])
@token_required
def get_library(current_user_token):
    a_user = current_user_token.token
    libraries = Library.query.filter_by(user_token = a_user).all()
    response = libraries_schema.dump(libraries)
    return jsonify(response)

@api.route('/libraries/<id>', methods = ['GET'])
@token_required
def get_single_library(current_user_token, id):
    library = Library.query.get(id)
    response = library_schema.dump(library)
    return jsonify(response)

@api.route('/libraries/<id>', methods = ['POST','PUT'])
@token_required
def update_library(current_user_token,id):
    library = library.query.get(id) 
    library.author_name = request.json['author_name']
    library.book_title = request.json['book_title']
    library.ISBN_number = request.json['ISBN_number']
    library.book_length = request.json['book_length']
    library.user_token = current_user_token.token

    db.session.commit()
    response = library_schema.dump(library)
    return jsonify(response)

@api.route('/libraries/<id>', methods = ['DELETE'])
@token_required
def delete_library(current_user_token, id):
    library = Library.query.get(id)
    db.session.delete(library)
    db.session.commit()
    response = library_schema.dump(library)
    return jsonify(response)