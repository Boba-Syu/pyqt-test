from flask import Flask, jsonify
from context import applicationContext
from server.database.database import UserInfo

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello, World!'


class HttpResult:
    def __init__(self, code, data):
        self.code = code
        self.data = data

    def to_json(self):
        return jsonify({
            'code': self.code,
            'data': self.data
        })

    @staticmethod
    def success(data):
        return HttpResult(200, data).to_json()

    @staticmethod
    def failure(data):
        return HttpResult(500, data).to_json()

@app.route('/user/all', methods=['GET'])
def user_find_all():
    userInfoList = (applicationContext.databaseClient.session
                    .query(UserInfo)
                    .all())
    return HttpResult.success([{
        'id': userInfo.id,
        'username': userInfo.username,
        'password': userInfo.password,
        'create_time': userInfo.create_time.strftime('%Y-%m-%d %H:%M:%S'),
        'update_time': userInfo.update_time.strftime('%Y-%m-%d %H:%M:%S'),
    } for userInfo in userInfoList])

@app.route('/user/id/<int:userId>', methods=['GET'])
def user(userId: int):
    userInfo = (applicationContext.databaseClient.session
                .query(UserInfo)
                .filter(UserInfo.id == userId)
                .first())
    return HttpResult.success({
        'id': userInfo.id,
        'username': userInfo.username,
        'password': userInfo.password,
        'create_time': userInfo.create_time.strftime('%Y-%m-%d %H:%M:%S'),
        'update_time': userInfo.update_time.strftime('%Y-%m-%d %H:%M:%S'),
    })
