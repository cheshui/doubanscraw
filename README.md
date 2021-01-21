# doubanscraw
上传节目名称获取豆瓣评分

1. 所需环境参见requirements.txt文件，建议使用虚拟环境安装依赖 pip install -r requirements.txt;运行过程中需要使用PhantomJS，请提前安装并配置环境变量；
2. 更改douban/settings.py中数据库配置信息，在MySQL中创建数据库
3. 在项目根目录依次运行如下命令，创建所需数据表：python manage.py makemigrations; python manage.py migrate;
4. 运行python manage.py runserver，打开浏览器访问http://localhost:8000/
