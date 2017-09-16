追梦人物的个人博客：http://zmrenwu.com/

----

## 在本地运行项目

1. 克隆项目到本地

   打开命令行，进入到保存项目的文件夹，输入如下命令：

   ```
   git clone https://github.com/zmrenwu/django-zmrenwu-blog.git
   ```

2. 创建并激活虚拟环境

   在命令行进入到保存虚拟环境的文件夹，输入如下命令创建并激活虚拟环境：

   ```
   virtualenv blogproject_env

   # windows
   blogproject_env\Scripts\activate

   # linux
   source blogproject_env/bin/activate
   ```

3. 安装项目依赖

   如果使用了虚拟环境，确保激活并进入了虚拟环境，在命令行进入项目所在的 django-zmrenwu-blog 文件夹，运行如下命令：

   ```
   pip install -r requirements/local.txt
   ```

4. 迁移数据库

   在上一步所在的位置运行如下命令迁移数据库：

   ```
   python manage.py migrate
   ```

5. 创建后台管理员账户

   在上一步所在的位置运行如下命令创建后台管理员账户

   ```
   python manage.py createsuperuser
   ```

6. 运行开发服务器

   在上一步所在的位置运行如下命令开启开发服务器：

   ```
   python manage.py runserver --settings=blogproject.settings.local
   ```

   在浏览器输入：127.0.0.1:8000

7. 进入后台发布文章

   在浏览器输入：127.0.0.1:8000/admin

   使用第 5 步创建的后台管理员账户登录

## 交流讨论和继续学习 Django

这里汇聚了大量经验丰富的 Django 开发者，遇到问题随时请教，以及获取更多的 Django 学习资料。

- Django 博客，更多 Django 开发文章和教程：[追梦人物的博客](http://zmrenwu.com/)
- Django 学习小组 QQ 群：561422498
- Django 学习交流论坛：[Pythonzhcn - Python 中文社区](http://www.pythonzh.cn/)
- Django 学习小组邮件列表：django_study@groups.163.com
- [Django 入门学习规划与资料推荐](http://zmrenwu.com/post/15/)