import grpc
from APIGateway import app
from flask import request, abort
from APIGateway.models import User
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)
from google.protobuf.json_format import MessageToDict
from APIGateway import api_gateway_pb2, api_gateway_pb2_grpc


users_service_stub = api_gateway_pb2_grpc.UsersAPIStub(grpc.insecure_channel('UsersService:50050'))  # gRPC stub to work with Users Service
images_service_stub = api_gateway_pb2_grpc.ImagesAPIStub(grpc.insecure_channel('ImagesService:50050'))  # gRPC stub to work with Images Service
cloudlets_service_stub = api_gateway_pb2_grpc.CloudletsAPIStub(grpc.insecure_channel('CloudletsService:50050'))  # gRPC stub to work with Cloudlets Service
scheduling_service_stub = api_gateway_pb2_grpc.SchedulingAPIStub(grpc.insecure_channel('SchedulingService:50050'))  # gRPC stub to work with Scheduling Service


@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(405)
def handler(error):
    return {'message': error.description}, error.code


# Checks the existence of a user with the specified username
@app.route('/check-user-existence')
def check_user_existence():
    username = request.values.get('username', type=str)
    response = users_service_stub.IsExist(api_gateway_pb2.User(username=username))
    return {'message': response.message}, response.code


# Creates a new user
@app.route('/user', methods=['POST'])
def add_user():
    response = users_service_stub.Create(api_gateway_pb2.User(first_name=request.values.get('first_name', type=str),
                                                              last_name=request.values.get('last_name', type=str),
                                                              username=request.values.get('username', type=str),
                                                              password=request.values.get('password', type=str)))
    if response.status.code == 201:
        user = User(username=response.user.username,
                    first_name=response.user.first_name,
                    last_name=response.user.last_name,
                    admin=response.user.admin)
        access_token = create_access_token(identity=user)
        return {'message': response.status.message,
                'access_token': access_token}, response.status.code
    else:
        return {'message': response.status.message}, response.status.code


# Returns information about the user
@app.route('/user')
@jwt_required
def user_data():
    claims = get_jwt_claims()
    username = request.values.get('username', type=str)

    if username not in [get_jwt_identity(), None] and not claims['admin']:
        abort(403)

    response = users_service_stub.Info(api_gateway_pb2.User(username=username))
    if response.status.code == 200:
        return {'message': response.status.message,
                'user': {
                    'username': response.user.username,
                    'first_name': response.user.first_name,
                    'last_name': response.user.last_name,
                    'admin': response.user.admin
                }}, response.status.code
    else:
        return {'message': response.status.message}, response.status.code


# Method for getting JWT access token by username and password
@app.route('/login')
def login():
    username = request.values.get('username', type=str)
    password = request.values.get('password', type=str)

    response = users_service_stub.Verify(api_gateway_pb2.User(username=username, password=password))
    if response.status.code == 200:
        user = User(username=response.user.username,
                    first_name=response.user.first_name,
                    last_name=response.user.last_name,
                    admin=response.user.admin)
        access_token = create_access_token(identity=user)
        return {'message': response.status.message, 'access_token': access_token}, response.status.code
    else:
        return {'message': response.status.message}, response.status.code


# Returns the list of fog application images
@app.route('/images')
@jwt_required
def images():
    username = request.values.get('username', type=str)
    claims = get_jwt_claims()

    if username != get_jwt_identity() and not claims['admin']:
        abort(403)

    response = images_service_stub.List(api_gateway_pb2.User(username=username))
    if response.status.code == 200:
        return {'message': response.status.message,
                'images': MessageToDict(response,
                                        including_default_value_fields=True,
                                        preserving_proto_field_name=True)['images']}, response.status.code
    else:
        return {'message': response.status.message}, response.status.code


@app.route('/image/<string:username>/<string:image_name>', methods=['GET', 'DELETE'])
@jwt_required
def image(username, image_name):
    claims = get_jwt_claims()
    if username != get_jwt_identity() and not claims['admin']:
        abort(403)

    # Returns information about specified image of fog application
    if request.method == 'GET':
        response = images_service_stub.Find(api_gateway_pb2.Image(name=username + '/' + image_name))
        return {'message': response.status.message,
                'image': MessageToDict(response.image,
                                       including_default_value_fields=False,
                                       preserving_proto_field_name=True)}, response.status.code
    # Removes the image of fog application
    elif request.method == 'DELETE':
        response = images_service_stub.Delete(api_gateway_pb2.Image(name=username + '/' + image_name))
        return {'message': response.message}, response.code
    else:
        abort(405)


# Returns a list of fog devices with the specified parameters
@app.route('/cloudlets', methods=['GET'])
@jwt_required
def cloudlets():
    claims = get_jwt_claims()

    if not claims['admin']:
        abort(403)
    params = {
        'id': request.values.get('id', type=str),
        'name': request.values.get('name', type=str),
        'cpu_cores': request.values.get('cpu_cores', type=int),
        'cpu_frequency': request.values.get('cpu_frequency', type=float),
        'ram_size': request.values.get('ram_size', type=int),
        'rom_size': request.values.get('rom_size', type=int),
        'os': request.values.get('os', type=str),
        'os_kernel': request.values.get('os_kernel', type=str),
        'ip': request.values.get('ip', type=str),
        'latitude': request.values.get('latitude', type=float),
        'longitude': request.values.get('longitude', type=float),
        'country': request.values.get('country', type=str),
        'region': request.values.get('region', type=str),
        'city': request.values.get('city', type=str)
    }

    cloudlet = api_gateway_pb2.Cloudlet()
    for key, value in params.items():
        if value:
            setattr(cloudlet, key, value)

    response = cloudlets_service_stub.Find(cloudlet)
    return {'message': response.status.message,
            'cloudlets': MessageToDict(response,
                                       including_default_value_fields=True,
                                       preserving_proto_field_name=True)['cloudlets']}, response.status.code


@app.route('/cluster/<string:cluster_id>', methods=['GET', 'DELETE'])
def cluster(cluster_id):
    # Returns the cluster state of IoT devices
    if request.method == 'GET':
        response = scheduling_service_stub.ClusterState(api_gateway_pb2.Cluster(id=cluster_id))
        return {'message': response.status.message,
                'cluster': MessageToDict(response.cluster,
                                         including_default_value_fields=False,
                                         preserving_proto_field_name=True)}, response.status.code
    # Removes an existing IoT device cluster
    elif request.method == 'DELETE':
        response = scheduling_service_stub.RemoveCluster(api_gateway_pb2.Cluster(id=cluster_id))
        return {'message': response.message}, response.code
    else:
        abort(405)


# Creates a new cluster of IoT devices
@app.route('/cluster', methods=['POST'])
def create_cluster():
    image = request.values.get('image', type=str)
    latitude = request.values.get('latitude', type=float)
    longitude = request.values.get('longitude', type=float)
    response = scheduling_service_stub.CreateCluster(api_gateway_pb2.Cluster(image=image,
                                                                             coordinates=api_gateway_pb2.Coordinates(latitude=latitude,
                                                                                                                     longitude=longitude)))
    return {'message': response.status.message,
            'cluster': MessageToDict(response.cluster,
                                     including_default_value_fields=False,
                                     preserving_proto_field_name=True)}, response.status.code
