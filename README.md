## 如何开发一个 Django 的生产级 Docker 化应用

> 目标：我们将之前实现的**Django + MySQL + Redis**  留言板应用 ，送上云端 ，轻松实现代码的持续集成和持续部署 。
> 
> 本项目代码维护在 [DaoCloud/python-django-cd-sample](https://github.com/DaoCloud/python-django-cd-sample)项目中 。



工欲善其器 ，必先利其器 。首先 ，你需要  `DaoCloud 帐号` `DaoCloud 帐号` `DaoCloud 帐号`



#### 云端镜像构建

> 比起本地创建，在云端创建会更简单。

第一步：在控制台点击「代码构建」。

![](http://help.daocloud.io/img/screenshots/features/build-flows/dashboard.png)

---

第二步：在「代码构建」的界面中点击「创建新项目」。

![](http://help.daocloud.io/img/screenshots/features/build-flows/build-flows-index.png)

---

第三步：为项目指定「项目名称」

稍等片刻 ，应用便在云端构建成咯



#### 云端部署镜像

第零步：在控制台点击「服务集成」，创建 mysql 和 redis 服务

第一步：在控制台点击「镜像仓库」。

第二步：在「代码构建」的界面中找到需要部署的镜像 ，点击「部署」。

第三步：按照为项目指定「项目名称」， 并在 「基础设置」中 绑定上  mysql 和 redis 服务 。

---

应用便在云端航行起来咯  ｡◕‿◕｡



### 云端持续集成

我们需要写一些测试代码 。

``` python
# /chat/tests.py
from django.test import TestCase
from django.test.client import Client


# Create your tests here.
class ChatTests(TestCase):
    client_class = Client

    def test(self):
        self.assertEqual(1 + 1, 2)

```

本地环境下可以使用以下命令来启动测试：

``` 
./manage.py test
```



当我们写完测试代码之后，我们需要一个持续集成环境来自动执行测试，报告项目的健康状况。

我们只需要在源代码的根目录放置 `daocloud.yml` 文件便可以接入 DaoCloud 持续集成系统，每一次源代码的变更都会触发一次 DaoCloud 持续集成。关于 `daocloud.yml` 的格式，请参考 **这里**。

daocloud.yml

``` yaml
image: daocloud/ci-python:2.7
services:
    - mysql
    - redis

env:
    - DAO_TEST = "True"
    - MYSQL_INSTANCE_NAME = "test"
    - MYSQL_USERNAME = "root"
    - MYSQL_PASSWORD = ""

install:
    - pip install coverage

before_script:
    - pip install -r requirements.txt

script:
    - coverage run --source='.' manage.py test
    - coverage report
```

之后的每一次 git push 都会触发持续集成 。

DaoCloud 在持续集成结束后还会有萌哒哒的结果报告。





#### 云端持续部署

只需要给 Git commit 打上标签

``` 
git tag v1.0
git push --tag
```

即可触发云端的镜像构建



在容器部署页面开启自动更新 。 即可完成云端的持续部署

