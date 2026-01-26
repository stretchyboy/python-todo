from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from todo import Todo, Category, db


class TodoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Todo
        sqla_session = db.session
        load_instance = True
        include_fk = True


class CategorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        sqla_session = db.session
        load_instance = True
