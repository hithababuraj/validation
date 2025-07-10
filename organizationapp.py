from flask import Flask,request,jsonify
from mongoengine import connect
from orgmodel import Organisation
from bson.errors import InvalidId
from bson import ObjectId
from mongoengine.errors import ValidationError

organizationapp= Flask(__name__)
connect(db='org_db',host='localhost',port=27017)

# Create organisation with Basic Validation
@organizationapp.route('/orgnisation', methods=['POST'])
def create_org():
    try:
        org = Organisation(**request.json)
        org.save()
        return {"message": "Organisation created", "id": str(org.id)}, 201
    except Exception as e:
        return {"error": "Validation Error", "details": str(e)}, 400

    

# list all organisation
@organizationapp.route('/organisation',methods=['GET'])
def list_organisation():
    org = Organisation.objects()
    data = []
    for o in org:
        d = o.to_mongo().to_dict()
        d['_id'] = str(d['_id'])
        data.append(d)
    return jsonify(data)

# update the organisation:
@organizationapp.route('/orginisation/<id>', methods=['PUT'])
def update_organisation(id):
    try:
        obj_id = ObjectId(id)
        data = request.json
        org = Organisation.objects(id=obj_id).first()
        if org:
            org.update(**data)
            updated_org = Organisation.objects(id=obj_id).first()
            org_dict = updated_org.to_mongo().to_dict()
            org_dict['_id'] = str(org_dict['_id'])  
            return jsonify(org_dict), 200
        else:
            return jsonify({"error": "Organisation not found"}), 404
    except (InvalidId, ValidationError):
        return jsonify({"error": "Invalid ID format"}), 400



# delete an organisation
@organizationapp.route('/orginisation/<id>', methods=['DELETE'])
def delete_organisation(id):
    try:
        org = Organisation.objects(id=id).first()
        if org:
            org.delete()
            return {"message": "Organisation deleted"}, 200
        else:
            return {"error": "Organisation not found"}, 404
    except Exception as e:
        return {"error": "Deletion Error", "details": str(e)}, 400





if __name__ == '__main__':
    organizationapp.run(debug=True)


    
        


