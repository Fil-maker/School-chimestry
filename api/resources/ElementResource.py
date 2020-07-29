import datetime

from flask import jsonify, g
from flask_restful import abort, Resource

from api.auth import token_auth
from api.data import db_session
from api.resources.parsers import element_parser_for_adding, element_parser_for_updating
from api.data.element import Element


def abort_if_element_not_found(func):
    def new_func(self, user_id):
        session = db_session.create_session()
        element = session.query(Element).get(user_id)
        if not element:
            abort(404, success=False, message=f"Element {user_id} not found")
        return func(self, user_id)

    return new_func


def only_for_current_user(func):
    def new_func(self, user_id):
        if user_id != g.current_user.id:
            abort(403, success=False)
        return func(self, user_id)

    return new_func


class UserResource(Resource):
    @abort_if_element_not_found
    def get(self, user_id):
        session = db_session.create_session()
        element = session.query(Element).get(user_id)
        return jsonify({'element': element.to_dict_myself()})

    @abort_if_element_not_found
    @token_auth.login_required
    @only_for_current_user
    def delete(self, user_id):
        session = db_session.create_session()
        element = session.query(Element).get(user_id)
        session.delete(element)
        session.commit()
        return jsonify({'success': True})

    @abort_if_element_not_found
    @token_auth.login_required
    @only_for_current_user
    def put(self, user_id):
        args = element_parser_for_updating.parse_args(strict=True)  # Вызовет ошибку, если запрос
        # будет содержать поля, которых нет в парсере
        session = db_session.create_session()
        element = session.query(Element).get(user_id)
        for key, value in args.items():
            if value is not None:
                exec(f"element.{key} = '{value}'")
        session.commit()
        return jsonify({'success': True})


class UserListResource(Resource):

    def get(self):
        session = db_session.create_session()
        element = session.query(Element).all()
        return jsonify({'users': [item.to_dict_myself() for item in element]})

    def post(self):
        args = element_parser_for_adding.parse_args(strict=True)
        session = db_session.create_session()
        element = Element(
            short_name=args['short_name'],
            full_name=args['full_name'],
            description=args['description'],
            mass=args['mass'],
            row=args['row'],
            column=args['column']
        )
        session.add(element)
        session.commit()
        return jsonify({'success': True})
