### 如何配置基于 Docker 持续集成的 Django 开发环境

> 目标：用 Docker 为搭建一套 持续集成的 Django 开发环境。
> 
> 本项目代码维护在 **[DaoCloud/python-django-sample](https://github.com/DaoCloud/python-django-sample)** 项目中。

### 前言

工欲善其事，必先利其器。这次我们将使用：

``` 
docker >= 1.8.0
docker-machine >= 0.4.1
docker-compose >= 1.4.0
```

等工具，实现基于 Docker 化持续性集成的 Django 开发环境。

#### Docker:

> 一款轻量级虚拟化容器的管理引擎。Docker Daemon、Client、Registry、Libcontainer……组成。

#### Docker-Client:

> Docker 架构中用户与 Docker Daemon 建立通信的客户端。

#### Docker-Daemon:

> Docker 架构中常驻后台的系统进程，负责接收处理用户发送的请求和管理所有的 Docker 容器，所谓的 **运行 Docker** 即代表 **运行 Docker Daemon**。

#### Docker-Machine

> Docker 官方推荐部署工具。帮助用户快速在运行环境中创建虚拟机服务节点。在虚拟机中安装并配置 Docker Client，使得 Docker Client 能快捷的与虚拟中的 Docker 建立通信。

#### Docker-Compose

> Docker 官方推荐服务编排工具。随着服务的复杂度增长，容器管理的配置项冗长。Compose 可有效缓解甚至解决容器部署的复杂性。

### 通过 Docker-Machine 安装 Docker

> 如果你是 Windows 或 Mac 用户 推荐阅读以下章节，如何使用 docker machine 安装与管理 docker 

``` bash
$ docker-machine create -d virtualbox dev;
INFO[0000] Creating CA: /Users/dev/.docker/machine/certs/ca.pem
INFO[0000] Creating client certificate: /Users/dev/.docker/machine/certs/cert.pem
INFO[0001] Downloading boot2docker.iso to /Users/dev/.docker/machine/cache/boot2docker.iso...
INFO[0035] Creating SSH key...
INFO[0035] Creating VirtualBox VM...
INFO[0043] Starting VirtualBox VM...
INFO[0044] Waiting for VM to start...
INFO[0094] "dev" has been created and is now the active machine.
To point your Docker client at it, run this in your shell: $(docker-machine env dev)
```

通过 `create` 命令启动了一台 machine 名为 dev，并安装好了 Docker。

> 因为 Create 命令在初始化的时候，会从海外下载一个 ISO 镜像。
> 
> 可以通过以下办法进行加速。
> 
> MAC
> 
> ``` bash
> $ mkdir ~/.boot2docker
> $ echo ISOURL = \"https://get.daocloud.io/boot2docker/boot2docker-lastest.iso\" > ~/.boot2docker/profile
> ```
> 
> Win
> 
> ``` bash
> $ ISOURL = "https://get.daocloud.io/boot2docker/boot2docker-lastest.iso"
> ```

通过 

``` bash
$ eval "$(docker-machine env dev)"
```

将当前的 Docker Client 和 dev 上的 Docker 建立起通信。

运行

``` bash
$ docker-machine ls
NAME   ACTIVE   DRIVER       STATE     URL
dev    *        virtualbox   Running   tcp://192.168.99.100:2376

```

查看当前 所有正在运行的 Machines。

``` bash
$ docker-machine start dev
Starting VM ...
```

启动 machine(dev)

``` bash
$ docker-machine ip dev
192.168.99.100
```

获取 machine(dev) 的 IP

``` bash
$ docker-machine ssh dev
Starting VM ...
```

通过 ssh 进入 machine(dev)

#### 通过 Docker Compose 编排应用

docker-compose.yml

``` yaml
web:
  build: .
  ports:
    - "8000:8000"
  links:
    - mysql:mysql
    - redis:redis
  env_file: .env
  volume: . /code
  command: /code/manage.py runserver 0.0.0.0:8000

mysql:
  image: mysql:latest
  environment:
    - MYSQL_DATABASE=django
    - MYSQL_ROOT_PASSWORD=mysql
  ports:
    - "3306:3306"

redis:
  image: redis:latest
  ports:
    - "6379:6379"

```

在这个文件中。我们定义了 3 个微服务 `web`、`mysql`、`redis`。

通过 `build/image` 为微服务指定了 docker 镜像。

通过 `links`，为 web 关联了 mysql 与 redis 服务。

通过 `ports`，为微服务映射相应的端口。

通过 `command`，为微服务配置启动时执行的命令（可覆盖 Dockerfile 里的声明）。

通过 `volume`，将源码挂载至服务中。保证代码即时更新至开发环境中。

万事俱备，现在让我们来让应用运行起俩，构建镜像并运行服务：

``` bash
$ docker-compose build
$ docker-compose up -d
```

别忘记要为项目初始化数据库哦：

``` bash
$ docker-compose run web /usr/local/bin/python manage.py migrate
```

这样我们的 Demo 就可以通过浏览器来访问了：）


！！！ 如果是使用 docker machine 的读者。你需要用

``` bash
$ docker-machine ip dev 
```

获取到实际运行环境的 IP，访问 `<ip>:8000`。


如果是 Linux 的读者，直接使用 127.0.0.1:8000 即可：

![](http://i3.tietuku.com/5a046900b9e8652b.png)

#### 总结

- docker machine 安装 docker
- docker compose 编排业务
- 通过 volume 挂载代码进入 容器
- 在开发状态下 容器只是单纯的运行环境
- 通过 `docker compose run web xxx` 执行 xxx 指令
