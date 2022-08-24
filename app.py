from flask import Flask
from flask_restful import Api, Resource, reqparse, marshal_with, fields
import models
from database import engine, session
import datetime

models.Base.metadata.create_all(bind=engine)

app = Flask(__name__)
api = Api(app)


todo_parser = reqparse.RequestParser()
todo_parser.add_argument("todo")
todo_marshal = {"id":fields.Integer,"todo":fields.String}
class Todo(Resource):
    @marshal_with(todo_marshal)
    def get(self, todo_id=None):
        if todo_id:
            #GET /todo/:id - get a todo
            todo = session.query(models.Todo).filter(models.Todo.id == todo_id).all()
            return todo
        else:
            #GET /todo - get list of todos
            todos = session.query(models.Todo).all()
            return todos

    def delete(self, todo_id):
        #DELETE /todo/:id - delete a todo
        todo = session.get(models.Todo, todo_id)
        session.delete(todo)
        session.commit()
        return 200

    def post(self):
        #POST /todo - create a new todo
        args = todo_parser.parse_args()
        newtodo = models.Todo(todo=args["todo"],created_at=datetime.datetime.now(),updated_at=datetime.datetime.now())
        session.add(newtodo)
        session.commit()
        return 200
    
    def put(self, todo_id):
        #PUT /todo/:id - update a todo
        args = todo_parser.parse_args()
        newdata = args["todo"]
        todo = session.get(models.Todo, todo_id)
        todo.todo = newdata
        session.commit()
        return "Ok",200

todo_comments_parser = reqparse.RequestParser()
todo_comments_parser.add_argument("comment")
todo_comment_marshal = {"id":fields.Integer,"todo_id":fields.Integer,"comment":fields.String}
class TodoComment(Resource):
    @marshal_with(todo_comment_marshal)
    def get(self, todo_id,comment_id = None):
        if todo_id and comment_id:
            # GET /todo/:id/comments/:comment_id - get a comment for a todo
            todo_comment = session.query(models.TodoComment).filter(models.TodoComment.id == comment_id).all()
            return todo_comment
        elif todo_id:
            # GET /todo/:id/comments - get comments for a todo
            todo_comments = session.query(models.TodoComment).filter(models.TodoComment.todo_id == todo_id).all()
            return todo_comments
        else:
            return "Please check id's and try again"

    def delete(self, todo_id,comment_id):
        # DELETE /todo/:id/comments/:comment_id - delete a comment for a todo
        todo_exists = session.get(models.Todo, todo_id)
        comment_exists = session.get(models.TodoComment,comment_id)
        if not todo_exists:
            return "Todo with id doesn't exist, try different one"
        if not comment_exists:
            return "Todo doesn't have a comment with that id on it, try a different one"
        todo_comment = session.get(models.TodoComment, comment_id)
        session.delete(todo_comment)
        session.commit()
    
    def put(self, todo_id, comment_id):
        # PUT /todo/:id/comments/:comment_id - update a comment for a todo
        todo_exists = session.get(models.Todo, todo_id)
        comment_exists = session.get(models.TodoComment,comment_id)
        if not todo_exists:
            return "Todo with id doesn't exist, try different one"
        if not comment_exists:
            return "Todo doesn't have a comment with that id on it, try a different one"

        args = todo_comments_parser.parse_args()
        new_comment = args["comment"]
        todo_comment = session.get(models.TodoComment, comment_id)
        todo_comment.comment = new_comment
        session.commit()
        return

    def post(self, todo_id):
        # POST /todo/:id/comments - create a comment for a todo
        todo_exists = session.get(models.Todo, todo_id)
        if not todo_exists:
            return "Todo with id doesn't exist, try different one"
        
        args = todo_comments_parser.parse_args()
        comment = args["comment"]
        newcomment = models.TodoComment(todo_id=todo_id,comment=comment,created_at=datetime.datetime.now(),updated_at=datetime.datetime.now())
        session.add(newcomment)
        session.commit()
        return

api.add_resource(TodoComment,'/todo/<todo_id>/comments','/todo/<todo_id>/comments/<comment_id>')
api.add_resource(Todo,"/todo","/todo/<todo_id>")

if __name__ == "__main__":
    app.run(debug=True)