

from flask_restx import Api, Resource, fields, Namespace
from flask import Blueprint, request, abort
from todo import Category, Todo, db
from auth import get_current_user

api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp, title="Todo API", version="1.0", description="Simple Todo API with categories")


# Model for output (response)
todo_model = api.model('Todo', {
    'id': fields.Integer(readOnly=True),
    'task': fields.String(required=True),
    'user_id': fields.String(readOnly=True),
    'category_id': fields.Integer(required=True),
    'done': fields.Boolean,
})

# Model for input (POST/PUT)
todo_input = api.model('TodoInput', {
    'task': fields.String(required=True),
    'category_id': fields.Integer(required=True),
    # 'done' is not required for POST, but allowed for PUT
    'done': fields.Boolean(default=False, required=False),
})

category_model = api.model('Category', {
    'id': fields.Integer(readOnly=True),
    'name': fields.String(required=True),
})

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
        return Category.query.all()

@api.route('/todos')
class TodoList(Resource):
    @api.marshal_list_with(todo_model)
    def get(self):
        """List all todos for the current user"""
        user = require_auth()
        return Todo.query.filter_by(user_id=user['id']).all()

    @api.expect(todo_input, validate=True)
    @api.marshal_with(todo_model, code=201)
    def post(self):
        """Create a new todo for the current user"""
        user = require_auth()
        data = api.payload
        todo = Todo(
            task=data['task'],
            category_id=data['category_id'],
            user_id=user['id'],
            done=data.get('done', False)
        )
        db.session.add(todo)
        db.session.commit()
        return todo, 201

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
        return todo

    @api.expect(todo_model, validate=True)
    @api.marshal_with(todo_model)
    def put(self, todo_id):
        """Update a todo by ID (must belong to user)"""
        user = require_auth()
        todo = Todo.query.get_or_404(todo_id)
        if todo.user_id != user['id']:
            abort(403)
        data = api.payload
        todo.task = data.get('task', todo.task)
        todo.category_id = data.get('category_id', todo.category_id)
        todo.done = data.get('done', todo.done)
        db.session.commit()
        return todo

    def delete(self, todo_id):
        """Delete a todo by ID (must belong to user)"""
        user = require_auth()
        todo = Todo.query.get_or_404(todo_id)
        if todo.user_id != user['id']:
            abort(403)
        db.session.delete(todo)
        db.session.commit()
        return '', 204
