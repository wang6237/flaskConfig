#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     app
   Description :
   Author :       wang6237
   date：          2020/4/11 11:03
-------------------------------------------------
   Change Activity:
                   2020/4/11 11:03
-------------------------------------------------
"""
__author__ = 'wang6237'

from flask import Flask, jsonify, abort, request, render_template, redirect
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_raw_jwt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import json
import hashlib
import configparser

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
app.config['JWT_IDENTITY_CLAIM'] = 'identity'  # Change this!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # Change this!
# app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']  # Change this!

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskConfig.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS '] = False
app._static_folder = 'static'
app.static_url_path = '/'
app.template_folder = 'templates'
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

db = SQLAlchemy(app)
jwt = JWTManager(app)

blacklist = set()


def Generate_pwd(password):
    return generate_password_hash(password)


def Check_pwd(pwd_hash, password):
    return check_password_hash(pwd_hash, password)


config = configparser.ConfigParser()
try:
    config.read('./config/config.ini')
    # print(config.sections())
except Exception as e:
    print(e)


def hashTool(arg1, arg2):
    m1 = hashlib.md5()
    m2 = hashlib.md5()
    m1.update(arg1.encode('utf-8'))
    m2.update(arg2.encode('utf-8'))
    print('Hash >>>>>>>>> ', m1.hexdigest(), m2.hexdigest())
    if m1.hexdigest() == m2.hexdigest():
        return True
    else:
        return False


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Environment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    path = db.Column(db.String(80), unique=True)
    content = db.Column(db.String(4096), nullable=False)
    comment = db.Column(db.String(180), nullable=False)

    def __repr__(self):
        return '<Environment %r>' % self.name


class ServiceTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    content = db.Column(db.String(2048), nullable=False)
    comment = db.Column(db.String(180), nullable=False)
    path = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<ServiceTemplate %r>' % self.name


class GetEtcdApi(object):
    """
    (host=(('127.0.0.1', 4001), ('127.0.0.1', 4002), ('127.0.0.1', 4003)))
    """

    def __init__(self, key):
        # config.get("etcd","etcdBaseUrl")
        self.url = config.get("etcd", "etcdBaseUrl") + key
        super(GetEtcdApi, self).__init__()

    def GetKey(self):
        try:
            r = requests.get(self.url)
            d = {'status_code': 200, 'data': r.json()}
            return d
        except requests.exceptions.ConnectionError:
            return {'status_code': -1, 'data': '无法连接到etcd....'}

    def DeleteKye(self):
        # self.c.delete(key)
        try:
            r = requests.delete(self.url + '?dir=true&recursive=true')
            # print(r.status_code)
            return r.json()
        except requests.exceptions.ConnectionError:
            return {'status_code': -1, 'data': '无法连接到etcd....'}

    def UpdateKey(self, value):
        data = {'value': value}
        try:
            r = requests.put(self.url, data=data)
            # print(r.status_code)
            return r.json()
        except requests.exceptions.ConnectionError:
            return {'status_code': -1, 'data': '无法连接到etcd....'}

    def CreateKey(self, value, mkdir):
        if mkdir:
            data = {'dir': mkdir}
            try:
                r = requests.put(self.url, data=data)
                # print(r.status_code)
                return r.json()
            except requests.exceptions.ConnectionError:
                return {'status_code': -1, 'data': '无法连接到etcd....'}
        else:
            data = {'value': value}
            try:
                r = requests.put(self.url, data=data)
                print(r.status_code)
                return r.json()
            except requests.exceptions.ConnectionError:
                return {'status_code': -1, 'data': '无法连接到etcd....'}

    def GetAllKey(self):
        try:
            r = requests.get(self.url + '/')
            return r.json()
        except requests.exceptions.ConnectionError:
            return {'status_code': -1, 'data': '无法连接到etcd....'}


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/v1/template', methods=['GET'])
@jwt_required
def getTemplate():
    """获取模板列表"""
    templ_lists = ServiceTemplate.query.all()
    print(templ_lists)
    templ_list = []
    if len(templ_lists) == 0:
        return jsonify({'total': 0, 'items': []})
    else:
        for t in templ_lists:
            i = {'name': t.name, 'content': json.loads(t.content), 'comment': t.comment, 'id': t.id, 'path': t.path}
            templ_list.append(i)
        return jsonify({'total': len(templ_list), 'items': templ_list})


@app.route('/v1/template/', methods=['POST'])
@jwt_required
def createTemplate():
    name = request.get_json()['name']
    content = request.get_json()['content']
    comment = request.get_json()['comment']
    path = request.get_json()['path']
    # if path[0] == '/':
    #     path =
    # print(content)
    templ = ServiceTemplate.query.filter_by(name=name).first()

    if templ is None:
        db.session.add(ServiceTemplate(name=name, content=json.dumps(content), comment=comment, path=path))
        db.session.commit()
        return jsonify({'type': 'success', 'msg': '添加成功'})
    else:
        return jsonify({'type': 'error', 'msg': '数据已存在，添加失败！！！'})


@app.route('/v1/template/<int:id>', methods=['PUT'])
@jwt_required
def editTemplate(id):
    name = request.get_json()['name']
    content = request.get_json()['content']
    comment = request.get_json()['comment']
    templ = ServiceTemplate.query.filter_by(name=name).first()
    if templ is None:
        return jsonify({'type': 'error', 'msg': '更新失败，数据不存在！！'})
    else:
        ServiceTemplate.query.filter_by(name=name).update({'content': json.dumps(content), 'comment': comment})
        return jsonify({'type': 'success', 'msg': '更新成功！'})


@app.route('/v1/template/<int:id>', methods=['DELETE'])
@jwt_required
def deleteTemplate(id):
    name = request.args.get('name')
    templ = ServiceTemplate.query.filter_by(name=name).first()
    if templ is None:
        return jsonify({'type': 'error', 'msg': '删除失败，数据不存在！！'})
    else:
        db.session.delete(templ)
        db.session.commit()
        return jsonify({'type': 'success', 'msg': '删除成功！'})


# @app.route('/v1/user', methods=['GET'])
# def getUser():
#     """获取模板列表"""
#     userinfo = {
#         'roles': ['admin'],
#         'introduction': 'I am a super administrator',
#         'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
#         'name': 'Super Admin'
#     }
#     return jsonify({userinfo}), 200


@app.route('/v1/user/', methods=['POST'])
@jwt_required
def createUser():
    username = request.get_json()['username']
    password = request.get_json()['password']
    role = request.get_json()['roles']
    email = request.get_json()['email']
    db.session.add(User(username=username, password=Generate_pwd(password), email=email, role=role))
    db.session.commit()
    return jsonify({'type': 'success', 'msg': '添加成功！'})


@app.route('/v1/user/info', methods=['GET'])
@jwt_required
def getUserInfo():
    userinfo = {
      'roles': ['admin'],
      'introduction': 'I am a super administrator',
      'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
      'name': 'Super Admin'
    }
    return jsonify(userinfo), 200


@app.route('/v1/user/<int:id>', methods=['PUT'])
@jwt_required
def editUser(id):
    username = request.get_json()['username']
    password = request.get_json()['password']
    role = request.get_json()['roles']
    email = request.get_json()['email']

    # pbkdf2:sha256 不在password中说明修改了密码，这里处理的不够严谨
    if 'pbkdf2:sha256' not in password:
        user = User.query.filter_by(username=username).update({'role': role, 'password': password, 'email': email})
    else:
        user = User.query.filter_by(username=username).update({'role': role, 'email': email})

    db.session.commit()
    return jsonify({'type': 'success', 'msg': '编辑成功！'})


@app.route('/v1/user/<int:id>', methods=['DELETE'])
@jwt_required
def deleteUser(id):
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    return jsonify({'type': 'success', 'msg': '删除成功！'})


@app.route('/v1/user/listinfo', methods=['GET'])
@jwt_required
def getUserList():
    users = User.query.all()
    userList = []
    for user in users:
        username = user.username
        password = user.password
        roles = user.role
        id = user.id
        email = user.email
        userList.append({'username': username, 'password': password, 'roles': roles, 'id': id, 'email': email})
    return jsonify({'total': len(users), 'items': userList})


@app.route('/v1/user/login', methods=['POST'])
def doLogin():
    username = request.get_json()['username']
    password = request.get_json()['password']
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    user_info = User.query.filter_by(username=username).first()
    print(user_info)
    if user_info is None:
        return jsonify({'msg': "Bad username"}), 401

    if not Check_pwd(user_info.password, password):
        return jsonify({'msg': "Bad password"}), 401
    access_token = create_access_token(identity=username)
    return jsonify({'token': access_token})


@app.route('/v1/user/logout', methods=['POST'])
@jwt_required
def doLogout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200


@app.route('/v1/env', methods=['GET'])
@jwt_required
def getEnv():
    env_lists = Environment.query.all()
    print(env_lists)
    env_list = []
    if len(env_lists) == 0:
        return jsonify({'total': 0, 'items': []})
    else:
        for e in env_lists:
            i = {'name': e.name, 'path': e.path, 'id': e.id, 'content': json.loads(e.content), 'comment': e.comment}
            env_list.append(i)
    return jsonify({'total': len(env_list), 'items': env_list})


@app.route('/v1/env/', methods=['POST'])
@jwt_required
def createEnv():
    name = request.get_json()['name']
    comment = request.get_json()['comment']
    template_name = request.get_json()['template_name']
    path = request.get_json()['path']
    if path[:-1] == '/':
        pass
    else:
        path = path + '/'
    envInfo = Environment.query.filter_by(name=name).first()
    if envInfo is None:
        c = []
        for i in template_name:
            templ = ServiceTemplate.query.filter_by(name=i).first()
            print(templ.path)
            if templ.path[0] == '/':
                templ.path = templ.path[1:]
                t = {
                    'name': i,
                    'path': path + templ.path,
                    'content': json.loads(templ.content)
                }
                c.append(t)
            else:
                t = {
                    'name': i,
                    'path': path + templ.path,
                    'content': json.loads(templ.content)
                }
                c.append(t)
            print('template>>>>>',c)
        print(c)
        db.session.add(Environment(name=name, content=json.dumps(c), comment=comment, path=path))
        db.session.commit()
        return jsonify({'total': 4, 'msg': '添加成功'})
    else:
        return jsonify({'type': 'error', 'msg': '添加失败，名称已存在！！'})


@app.route('/v1/env/<int:id>', methods=['PUT'])
@jwt_required
def editEnv(id):
    name = request.get_json()['name']
    content = request.get_json()['content']
    template_name = request.get_json()['template_name']
    comment = request.get_json()['comment']
    path = request.get_json()['path']
    envInfo = Environment.query.filter_by(path=path).first()
    if envInfo is None:
        return jsonify({'type': 'error', 'msg': '更新失败，数据不存在！'})
    else:
        c = content
        for i in template_name:
            templ = ServiceTemplate.query.filter_by(name=i).first()
            if templ.path[0] == '/':
                templ.path = templ.path[1:]
                t = {
                    'name': i,
                    'path': path + templ.path,
                    'content': json.loads(templ.content)
                }
                c.append(t)
        Environment.query.filter_by(path=path).update({'name': name, 'comment': comment, 'content': json.dumps(c)})
        return jsonify({'type': 'success', 'msg': '更新成功'})


@app.route('/v1/env/<int:id>', methods=['DELETE'])
@jwt_required
def deleteEnv(id):
    # id = request.args.get('id')
    # print(id)
    envInfo = Environment.query.filter_by(id=id).first()
    if envInfo is None:
        return jsonify({'type': 'error', 'msg': '删除失败，数据不存在！'})
    else:
        etcdServer = GetEtcdApi(envInfo.path)
        etcdServer.DeleteKye()
        db.session.delete(envInfo)
        db.session.commit()
        return jsonify({'type': 'success', 'msg': '删除成功！'})


@app.route('/v1/env/sync/', methods=['POST'])
@jwt_required
def doSync():
    name = request.get_json()['name']
    content = request.get_json()['content']
    path = request.get_json()['path']
    etcdServer = GetEtcdApi(path)
    r = etcdServer.CreateKey(content, mkdir=False)
    return jsonify({'type': 'success', 'msg': '同步成功！'})


@app.route('/v1/env/sync/<int:id>', methods=['DELETE'])
@jwt_required
def doSyncDelete(id):
    path = request.args.get('path')
    envId = request.args.get('envId')
    etcdServer = GetEtcdApi(path)
    envInfo = Environment.query.filter_by(id=envId).first()
    if envInfo is None:
        return jsonify({'type': 'error', 'msg': '删除失败！数据不存在！'})
    else:
        data = json.loads(envInfo.content)
        for index, i in enumerate(data):
            # print(i['path'], index)
            if i['path'] == path:
                data.pop(index)
                r = etcdServer.DeleteKye()
        data = json.dumps(data)
        Environment.query.filter_by(id=envId).update({'content': data})
        return jsonify({'type': 'success', 'msg': '删除成功'})


@app.route('/v1/env/sync/state/', methods=['PUT'])
@jwt_required
def editState():
    path = request.get_json()['path']
    content = request.get_json()['content']
    envId = request.get_json()['envId']
    # envInfo = Environment.query.filter_by(id=envId).first()
    etcdServer = GetEtcdApi(path)
    c = etcdServer.GetKey()
    print(c)
    # print()
    if c['status_code'] == 200:
        r = hashTool(content, c['data']['node']['value'])
        if r:
            return jsonify({'state': 0, 'items': c['data']['node']['value']})
        else:
            return jsonify({'state': 1, 'items': c['data']['node']['value']})
    else:
        return jsonify({'state': 1, 'items': []})


if __name__ == '__main__':
    app.run(debug=True)
