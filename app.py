from flask import Flask, jsonify, request
import expensive_mongo as em
from flask_cors import CORS, cross_origin
from google.oauth2 import id_token
from google.auth.transport import requests
import jwt
import datetime
import os
import time
from dotenv import load_dotenv
print( f"jwtwwww: {jwt.__file__}")
load_dotenv()
app = Flask(__name__)
CORS(app)
# CORS(app, resources={r"/google-auth.*": {"origins": "http://localhost:5173"}})

SECRET_KEY = os.getenv('SECRET_KEY')
CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')  # 從 .env 文件或環境中獲取 Google 客戶端 ID
print(f"CLIENT_ID222: {CLIENT_ID}")


@app.route('/items/', methods=['GET'])
def get_items():
    return jsonify(em.get_items())


@app.route('/item/', methods=['POST'])
def add_item():
    data = request.get_json()
    print(data)
    if em.add_item(data['name'], data['price'], data['type']):
        result = jsonify(message='add item successful')
    else:
        result = jsonify(message='add item failed')
    return result


@app.route('/item/<obj_id>', methods=['DELETE'])
def delete_item(obj_id):
    if em.remove_item(obj_id):
        result = jsonify(message='delete item successful')
    else:
        result = jsonify(message='delete item failed')
    return result

@app.route('/register/', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    print(data)
    
    # 調用 add_user 函數，並處理結果
    result = em.add_user(username, email, password)
    if 'error' in result:
        response = jsonify(message=result['error'])
        response.status_code = 400
    else:
        response = jsonify(message=result['message'])
        response.status_code = 201
    
    return response

# 登入用戶（電子郵件和密碼）
@app.route('/login/', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # 假設 em.get_user_by_email() 能查詢用戶
    user = em.get_user_by_email(email)
    if user and em.verify_password(password, user['password']):
        # 如果用戶存在且密碼驗證成功，生成 JWT Token
        jwt_token = jwt.encode({
            'email': email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm='HS256')
        
        response = jsonify({
            'message': 'Login successful',
            'token': jwt_token
        })
        response.status_code = 200
    else:
        response = jsonify(message='Invalid email or password')
        response.status_code = 401

    return response

# Google OAuth 登入/註冊
@app.route('/google-auth/', methods=['POST'])
def google_auth():
    data = request.get_json()
    token = data.get('credential')
    try:
        # 驗證 ID Token
        id_info = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
        
        # 若驗證通過，可從 id_info 中取得使用者資訊
        user_email = id_info.get('email')
        user_name = id_info.get('name')
        # user_picture = id_info.get('picture') # 若您需要用戶頭像，可以在後續的 UI 顯示中使用

        # 使用 user_email 來查詢或建立用戶
        # 假設 add_user(username, email, password=None) 是您的註冊函式
        user = em.add_user(user_name, user_email, password=None)
        
        if 'error' in user and user['error'] == 'User already exists':
            # 用戶已存在資料庫中，表示是登入動作
            user_info = em.get_user_by_email(user_email)  # 假設有此函數取得使用者完整資料
            message = 'User logged in successfully'
        else:
            # 新用戶已成功註冊
            user_info = em.get_user_by_email(user_email)
            message = 'User registered successfully'

        # 為該用戶生成 JWT Token
        jwt_token = jwt.encode({
            'email': user_email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm='HS256')

        response = jsonify({
            'message': message,
            'token': jwt_token,
            'user_info': user_info
        })
        response.status_code = 200
        return response

    except ValueError as e:
        # 驗證失敗
        print("ID Token 驗證失敗:", e)
        response = jsonify({'error': 'Invalid token'})
        response.status_code = 401
        return response
    

# @app.route('/google-auth/', methods=['POST'])
# def google_auth():
    
#     # 使用者端傳來的 ID Token（此處僅為範例）
#     # id_token_str = "使用者傳入的ID_TOKEN"
#     data = request.get_json()
#     token = data.get('credential')
#     try:
#         # 驗證 ID Token
#         id_info = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
        
#         # 若驗證通過，可從 id_info 中取得使用者資訊
#         user_id = id_info.get('sub')
#         user_email = id_info.get('email')
#         user_name = id_info.get('name')
#         user_picture = id_info.get('picture')

#         # 在此可進行後續處理，如查詢或建立資料庫中使用者資料
#         print("驗證成功！")
#         print("User ID:", user_id)
#         print("User Email:", user_email)
#         print("User Name:", user_name)
#         print("User Picture:", user_picture)
        
#         return id_info  # 視需求決定回傳值

#     except ValueError as e:
#         # 驗證失敗
#         print("ID Token 驗證失敗:", e)
#         return None


# def google_auth():
#     data = request.get_json()
#     token = data.get('credential')
#     print(f"Received token: {token}")

#     try:
#         if not token:
#             raise ValueError("No token provided")
#         print("Before jwt.encode(), SECRET_KEY =", SECRET_KEY, type(SECRET_KEY))
#         # 尝试解码 JWT（无签名验证）
#         unverified_claims = jwt.decode(token, options={"verify_signature": False})
#         token_nbf = unverified_claims.get('nbf')
#         print(f"Token 'nbf' time: {token_nbf}")

#         # 验证 Google ID Token
#         # 注意这里如果 CLIENT_ID 未正确设置，会抛出异常
#         id_info = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
        
#         # 获取用户信息
#         email = id_info.get('email')
#         username = id_info.get('name')

#         user = em.add_user(username, email, password=None)
#         if 'error' in user and user['error'] == 'User already exists':
#             message = 'User logged in successfully'
#         else:
#             message = 'User registered successfully'

#         exp_timestamp = int(time.time()) + 3600
#         # 生成 JWT Token
#         jwt_token = jwt.encode({
#             'email': email,
#             'exp': exp_timestamp
#         }, SECRET_KEY, algorithm='HS256')

#         response = jsonify({
#             'message': message,
#             'token': jwt_token
#         })
#         response.status_code = 200

#     except ValueError as e:
#         print(f"ValueError: {e}")
#         response = jsonify(message='Invalid token')
#         response.status_code = 400
#     except Exception as e:
#         # 捕获所有异常防止返回默认HTML错误页面
#         print(f"Unexpected error: {e}")
#         response = jsonify(message='Server internal error')
#         response.status_code = 500

#     return response

# @app.route('/google-auth/', methods=['POST'])
# @cross_origin()
# def google_auth():
#     data = request.get_json()
#     token = data.get('credential')
#     print(f"Received token: {token}")

    
#     try:
#         # 打印服务器当前时间
#         current_time = int(time.time())
#         print(f"Server current time: {current_time}")

#         # 解码令牌以获取 nbf 时间
#         unverified_claims = jwt.decode(token, options={"verify_signature": False})
#         token_nbf = unverified_claims.get('nbf')
#         print(f"Token 'nbf' time: {token_nbf}")
#         # 驗證 Google ID Token
#         id_info = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
        
#         # 驗證通過後獲取用戶信息
#         email = id_info.get('email')
#         username = id_info.get('name')

#         # 查找或創建用戶
#         user = em.add_user(username, email, password=None)
#         if 'error' in user and user['error'] == 'User already exists':
#             user_info = em.get_user_by_email(email)  # 假設有這個函數獲取用戶信息
#             message = 'User logged in successfully'
#         else:
#             message = 'User registered successfully'

#         # 為該用戶生成 JWT Token
#         jwt_token = jwt.encode({
#             'email': email,
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
#         }, SECRET_KEY, algorithm='HS256')

#         response = jsonify({
#             'message': message,
#             'token': jwt_token
#         })
#         response.status_code = 200

#     except ValueError as e:
#         # ID Token 驗證失敗
#         print(f"Token verification error: {e}")
#         # ID Token 驗證失敗
#         response = jsonify(message='Invalid token')
#         response.status_code = 400

#     return response

if __name__ == '__main__':
    app.run(debug=True)
