from APIGateway import jwt


# Adds fields with information about the user to the token when creating a token
@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'admin': user.admin
    }


# Defines the identity when creating a token
@jwt.user_identity_loader
def user_identity_lookup(user):
    if isinstance(user, User):
        return user.username
    else:
        return user


# User class for storing information when creating a token
class User:
    def __init__(self, username, first_name, last_name, admin):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.admin = admin

    def __repr__(self):
        return f"User('{self.username}', '{self.first_name}', '{self.last_name}', '{self.admin}')"
