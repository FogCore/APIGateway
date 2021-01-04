# API Gateway

The service provides only RESTfull API using JSON.

**All API methods can return:**

1. **code**:500, {**message**: "An internal server error has occurred."}



## `GET` /check-user-existence

Checks the existence of a user with the specified username.

#### Parameters:

1. **username**. Unique user login in the system.

#### Result:

1. **code**:200, {**message**: "An account with this username already exists."}
2. **code**:404, {**message**: "An account with this username not found."}
3. **code**:422, {**message**: "Username parameter is missing."}



## `POST` /user

Creates a new user.

#### Parameters:

1. **username**. Unique user login in the system.
2. **first_name**.
3. **last_name**.
4. **password**.

#### Result:

1. **code**:201, {**message**: "User account has been created successfully.", **access_token**: string}
2. **code**:409, {**message**: "That username is taken. Please choose a different one."}
3. **code**:422, {**message**: "First name, last name, username and password parameters are required."}

## `GET` /user

Returns information about the user.

#### Headers:

1. **Authorization**: Bearer access_token

#### Parameters:

1. **username**. Unique user login in the system.

#### Result:

1. **code**:200, {**message**: "User with this username exists.", **user**: {**username**: string, **first_name**: string, **last_name**: string, **admin**: bool}}
2. **code**:401, {**message**: "Missing Authorization Header"}
3. **code**:403, {**message**: "You don't have the permission to access the requested resource. It is either read-protected or not readable by the server."}
4. **code**:404, {**message**: "User with this username not found."}
5. **code**:422, {**message**: "Username parameter is required."}



## `GET` /login

Method for getting JWT access token by username and password.

#### Parameters:

1. **username**. Unique user login in the system..
2. **password**.

#### Result:

1. **code**:200, {**message**: "Username and password are correct.", **access_token**: string}
2. **code**:401, {**message**: "Incorrect username or password."}
3. **code**:422, {**message**: "Username and password parameters are required."}


**The reported project was supported by RFBR, research project No. 18-07-01224**
