# flaskConfig
利用flask写的基于etcd的配置中心

python 3.7.7, flask 1.0.3, 详见requirements.txt

页面基于
[vue-element-admin](https://panjiachen.github.io/vue-element-admin-site/zh/)
实现的

```bash
git clone https://github.com/wang6237/flaskConfig.git
cd flaskConfig
pip install -r requirements.txt
python init_db.py
python app.py
```

## install dependency
```
npm install
```
# develop
```bash
npm run dev
```

This will automatically open http://localhost:9528

## Build

```bash
# build for test environment
npm run build:stage

# build for production environment
npm run build:prod
```

