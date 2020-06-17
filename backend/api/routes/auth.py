# import json
# from flask import jsonify, request, g

#
# @app.route('/user')
# @auth.login_required
# def get_token():
#     return jsonify({'user': User.Schema().dump(g.user)})
#
#
# @app.route('/login', methods=['POST'])
# def login():
#     data = json.loads(request.data)
#     username = data['username']
#     password = data['password']
#
#     user = verify_password(username, password)
#     if not user:
#         return 'Unauthorized', 401
#
#     token = user.generate_auth_token()
#     data = jsonify({'token': token.decode('utf-8')})
#     return data, 200
#
#
# @app.route('/logout', methods=['POST'])
# @auth.login_required
# def logout():
#     return 'Ok', 200