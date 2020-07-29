import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from api.data.db_session import SqlAlchemyBase


class Element(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'elements'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    short_name = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True, index=True)
    full_name = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True, index=True)
    description = sqlalchemy.Column(sqlalchemy.String)
    mass = sqlalchemy.Column(sqlalchemy.Float)
    row, column = sqlalchemy.Column(sqlalchemy.Integer), sqlalchemy.Column(sqlalchemy.Integer)

    def to_dict_myself(self):
        return self.to_dict(only=('id', 'short_name', 'full_name', 'description', 'mass', 'row', 'column'))
