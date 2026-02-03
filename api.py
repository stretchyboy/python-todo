from flask_restx import Api, Resource, fields, Namespace
from flask import Blueprint, request, abort
from flask_restx import Api, Resource, Namespace, fields
from flask import Blueprint, request, abort
from todo import Category, Todo, db
from auth import get_current_user
from schemas import TodoSchema, CategorySchema


api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp, title="Todo API", version="1.0", 
          description="Simple Todo API with categories")


# For docs only
todo_model = api.model('Todo', {
    'id': fields.Integer(readOnly=True),
    'task': fields.String(required=True),
    'user_id': fields.String(readOnly=True),
    'category_id': fields.Integer(required=True),
    'done': fields.Boolean,
})

todo_input = api.model('TodoInput', {
    'task': fields.String(required=True),
    'category_id': fields.Integer(required=True),
    'done': fields.Boolean(default=False, required=False),
})

category_model = api.model('Category', {
    'id': fields.Integer(readOnly=True),
    'name': fields.String(required=True),
})

todo_schema = TodoSchema()
category_schema = CategorySchema()


def require_auth():
    user = get_current_user()
    if not user or not user.get('id'):
        abort(401)
    return user


@api.route('/categories')
class CategoryList(Resource):
    @api.marshal_list_with(category_model)
    def get(self):
        """List all categories"""
        categories = Category.query.all()
        return category_schema.dump(categories, many=True)


@api.route('/todos')
class TodoList(Resource):
    @api.marshal_list_with(todo_model)
    def get(self):
        """List all todos for the current user"""
        user = require_auth()
        todos = Todo.query.filter_by(user_id=user['id']).all()
        return todo_schema.dump(todos, many=True)

    @api.expect(todo_input, validate=True)
    @api.marshal_with(todo_model, code=201)
    def post(self):
        """Create a new todo for the current user"""
        user = require_auth()
        data = request.get_json()
        errors = todo_schema.validate(data, partial=False)
        if errors:
            return errors, 400
        todo = Todo(
            task=data['task'],
            category_id=data['category_id'],
            user_id=user['id'],
            done=data.get('done', False)
        )
        db.session.add(todo)
        db.session.commit()
        return todo_schema.dump(todo), 201


@api.route('/todos/<int:todo_id>')
@api.response(404, 'Todo not found')
class TodoResource(Resource):
    @api.marshal_with(todo_model)
    def get(self, todo_id):
        """Get a todo by ID (must belong to user)"""
        user = require_auth()
        todo = Todo.query.get_or_404(todo_id)
        if todo.user_id != user['id']:
            abort(403)
        return todo_schema.dump(todo)

    @api.expect(todo_input, validate=True)
    @api.marshal_with(todo_model)
    def put(self, todo_id):
        """Update a todo by ID (must belong to user)"""
        user = require_auth()
        todo = Todo.query.get_or_404(todo_id)
        if todo.user_id != user['id']:
            abort(403)
        data = request.get_json()
        errors = todo_schema.validate(data, partial=True)
        if errors:
            return errors, 400
        todo.task = data.get('task', todo.task)
        todo.category_id = data.get('category_id', todo.category_id)
        todo.done = data.get('done', todo.done)
        db.session.commit()
        return todo_schema.dump(todo)

    def delete(self, todo_id):
        """Delete a todo by ID (must belong to user)"""
        user = require_auth()
        todo = Todo.query.get_or_404(todo_id)
        if todo.user_id != user['id']:
            abort(403)
        db.session.delete(todo)
        db.session.commit()
        return '', 204
        data = api.payload
