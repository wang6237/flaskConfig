#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     init_db
   Description :
   Author :       wang6237
   date：          2020/4/11 13:59
-------------------------------------------------
   Change Activity:
                   2020/4/11 13:59
-------------------------------------------------
"""
__author__ = 'wang6237'

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from models.EtcdModel import Etcd
# from models.ProjectModel import Project
# from models.ContrlModel import Control
# from models.UserModel import User
# from models import db, reset_database
from app import db, User
from app import Generate_pwd

db.create_all()
db.session.add(User(username='admin', password=Generate_pwd('111111'), email='ykwang@vip.qq.com', role='admin'))
# db.session.add(Project(''))
# db.session.commit()
# print(User.query.filter_by(username='test').update({'role': 'dev'}))
# db.session.add(User)
db.session.commit()

