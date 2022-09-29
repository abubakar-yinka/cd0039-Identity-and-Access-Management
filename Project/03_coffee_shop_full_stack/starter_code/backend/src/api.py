import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@DONE uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
# db_drop_and_create_all()

# ROUTES
'''
@DONE implement endpoint - DONE
    GET /drinks
        it should be a public endpoint - DONE
        it should contain only the drink.short() data representation - DONE
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks - DONE
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks')
def get_drinks():
    try:
        drinks = Drink.query.all()
        drinks = [drink.short() for drink in drinks]
        return jsonify({
            'success': True,
            'drinks': drinks
        }), 200
    except:
        abort(422)


'''
@DONE implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission: DONE
        it should contain the drink.long() data representation: DONE
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks - DONE
        or appropriate status code indicating reason for failure - DONE
'''


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    try:
        print(payload)
        drinks = Drink.query.all()
        drinks = [drink.long() for drink in drinks]
        return jsonify({
            'success': True,
            'drinks': drinks
        }), 200
    except:
        abort(422)


'''
@DONE implement endpoint
    POST /drinks
        it should create a new row in the drinks table - DONE
        it should require the 'post:drinks' permission - DONE
        it should contain the drink.long() data representation - DONE
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink - DONE
        or appropriate status code indicating reason for failure - DONE
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    try:
        body = request.get_json()
        new_title = body.get('title', None)
        if not new_title:
            abort(422)
        new_recipe = body.get('recipe', None)
        if not new_recipe:
            abort(422)
        drink = Drink(title=new_title, recipe=json.dumps(new_recipe))
        drink.insert()
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        }), 200
    except:
        abort(422)


'''
@DONE implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found - DONE
        it should update the corresponding row for <id> - DONE
        it should require the 'patch:drinks' permission - DONE
        it should contain the drink.long() data representation - DONE
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink - DONE
        or appropriate status code indicating reason for failure - DONE
'''


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, id):
    try:
        body = request.get_json()
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if not drink:
            abort(404)
        new_title = body.get('title', None)
        if new_title:
            drink.title = new_title
        new_recipe = body.get('recipe', None)
        if new_recipe:
            drink.recipe = json.dumps(new_recipe)
        drink.update()
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        }), 200
    except:
        abort(404)


'''
@DONE implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found - DONE
        it should delete the corresponding row for <id> - DONE
        it should require the 'delete:drinks' permission - DONE
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record - DONE
        or appropriate status code indicating reason for failure - DONE
'''


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    try:
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if not drink:
            abort(404)
        drink.delete()
        return jsonify({
            'success': True,
            'delete': id
        }), 200
    except:
        abort(404)


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@DONE implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@DONE implement error handler for 404
    error handler should conform to general task above
'''


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


'''
@DONE implement error handler for AuthError
    error handler should conform to general task above
'''


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code
