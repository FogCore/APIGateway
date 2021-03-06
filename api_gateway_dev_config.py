# Flask Options
DEBUG = True

# General JWT Options
JWT_TOKEN_LOCATION = ['headers']
JWT_ACCESS_TOKEN_EXPIRES = False
JWT_ALGORITHM = 'ES512'
JWT_PUBLIC_KEY = '''-----BEGIN PUBLIC KEY-----
MIGbMBAGByqGSM49AgEGBSuBBAAjA4GGAAQBsg95IYXv1yEIBJhfSRf+OSC8kgPA
kYOFGe7vc9BA/MMMJV7IfmdssxWjj7oNW7nD5XfIBQXtUNnj/K8urQTIo5gAdxap
QqUfSCs7sBWiZXQGWwwBBhSw7bLbFvU5i87B1qISSjQEQj0/mf97qd/suIlESXlB
M1tWZ3lONvaDtSl8cCI=
-----END PUBLIC KEY-----'''
JWT_PRIVATE_KEY = '''-----BEGIN EC PRIVATE KEY-----
MIHbAgEBBEHXzgMiDLQ+wG7WCbnVqw5VTZ7HUnMszq7Ck2bXLtj58XuV1+IOHPEo
xFrdwsBIe+U+SRyixH2z/PfwCyC+GR7gjKAHBgUrgQQAI6GBiQOBhgAEAbIPeSGF
79chCASYX0kX/jkgvJIDwJGDhRnu73PQQPzDDCVeyH5nbLMVo4+6DVu5w+V3yAUF
7VDZ4/yvLq0EyKOYAHcWqUKlH0grO7AVomV0BlsMAQYUsO2y2xb1OYvOwdaiEko0
BEI9P5n/e6nf7LiJREl5QTNbVmd5Tjb2g7UpfHAi
-----END EC PRIVATE KEY-----'''
JWT_IDENTITY_CLAIM = 'sub'
JWT_ERROR_MESSAGE_KEY = 'message'
JWT_USER_CLAIMS = 'user_claims'

# Header JWT Options
JWT_HEADER_NAME = 'Authorization'
JWT_HEADER_TYPE = 'Bearer'
