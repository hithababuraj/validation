from flask import Flask, request, jsonify
from mongoengine import connect
from models import User
from datetime import datetime



app = Flask(__name__)
connect(db="validation_db", host="localhost", port=27017)

# Create User with Basic Validation
@app.route('/users', methods=['POST'])
def create_user():
    try:
        user = User(**request.json)
        user.save()
        return {"message": "User created", "id": str(user.id)}, 201
    except Exception as e:
        return {"error": str(e)}, 400


# Get All Users with Filters - {age >20, age <10}
@app.route('/users/filter', methods=['GET'])
def filter_users():
    users1 = User.objects(age__gt=20)
    users2 = User.objects(age__lt=10)

    all_users = list(users1) + list(users2)

    data = []
    for user in all_users:
        u = user.to_mongo().to_dict()
        u['_id'] = str(u['_id'])
        data.append(u)

    return jsonify(data)


# Get Single User by ID
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = User.objects(id=id).first()
    if user:
        u = user.to_mongo().to_dict()
        u['_id'] = str(u['_id']) 
        return jsonify(u)
    return jsonify({"error": "User not found"}), 404


# Update User based on id
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    data = request.json  
    user = User.objects(id=id).first()

    if user:
        user.update(**data)  
        updated_user = User.objects(id=id).first()
        user_dict = updated_user.to_mongo().to_dict()
        user_dict['_id'] = str(user_dict['_id'])  
        return jsonify(user_dict), 200
    else:
        return jsonify({"error": "User not found"}), 404

# Delete User
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    data=request.json
    user=User.objects(id=id).first()

    if user:
        user.delete()
        return jsonify("user deleted")
    else:
        return jsonify("user not found")
    
# User Login (Check email/password match and return success msg)
@app.route('/login', methods=['POST'])
def login():
    data=request.json
    email=data.get('email')
    password=data.get('password')
    user=User.objects(email=email,password=password).first()
    if user:
        return jsonify("Login Sucessfull")
    else:
        return jsonify("Invalid email or Password")
    

# Search Users based on email or name
@app.route('/users/search', methods=['GET'])
def search_users():
    keyword = request.args.get('q')

    users_by_email = User.objects(email__icontains=keyword)
    users_by_name = User.objects(name__icontains=keyword)

    all_users = list(users_by_email) + [u for u in users_by_name if u not in users_by_email]

    data = []
    for user in all_users:
        u = user.to_mongo().to_dict()
        u['_id'] = str(u['_id'])
        data.append(u)

    return jsonify(data)



if __name__ == '__main__':
    app.run(debug=True)


