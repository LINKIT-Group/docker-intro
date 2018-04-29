---
layout: layout.html
---

# Docker basics Hands-on

## Agenda
- [Before you start](#before-you-start)
- [Setup](#setup)
- [1. Basic Docker](#basic-docker)
- [2. Docker Applications](#docker-applications)
    - [2.1 Static Sites](#static-site)
    - [2.2 Docker Images](#docker-images)
    - [2.3 A First Image](#our-image)
- [3. Closer to real-life](#closer-to-real-life)
    - [3.1 Docker Network](#docker-network)
    - [3.2 Docker Compose](#docker-compose)
- [4. Next Steps](#next-steps)

> Note1: This course was intended as an Introduction to Docker for OutSystem developers and it goes along a `.key` presentation that is not on this repository.

>Note2: Built with Docker **1.8**.

------------------------------

<a id="before-you-start"></a>
### Before you start
This is a docker tutorial... thus a having Docker on your machine is fundamental. Besides that, having basic knowledge and comfort using the command line is also relevant.

<a id="setup"></a>
### Setup
Since the majority here is an OutSystem developer, I am assuming you are using Windows machines. Back in the days, running Docker on Windows was quite a hassle. But with the impressive growth and usage of Docker in the last years, the community around and Docker.inc spent a lot of time making the onboarding process smoothier. The *getting started* guide on Docker makes it really easy to setup docker on your machine. So just click on your OS to be redirected to the correct page: [Mac](https://www.docker.com/products/docker#/mac), [Linux](https://www.docker.com/products/docker#/linux) or [Windows](https://www.docker.com/products/docker#/windows).

To test your docker installation, just run the basic `hello-world` image:
```
$ docker run hello-world
```
___________

<a id="basic-docker"></a>
## 1. Basic Docker
I hope you know a bit about Unix and the Ubuntu distribution. Why? Because we will start to see a bit how powerful Docker is and how to use the client.
```bash
$ docker pull ubuntu

Using default tag: latest
latest: Pulling from library/ubuntu
...
```

The `pull` command just fetches the Ubuntu [**image**](https://hub.docker.com/_/ubuntu/) from the [**Docker registry**](https://hub.docker.com/explore/) and saves it to our system. You can think of it as a **.vbox** file, but as we have seen on the slides, a much smaller and simpler version. 
<br> As of the The Docker Registry is just like a github repository, but insteand of pushing/pulling code from accounts you push/pull docker images (sometimes called an artifact). Companies can use several types of registries, keep it public, private and so on.

To see all images that you have, you can use the `docker images` command.
```bash
$ docker images

REPOSITORY                                               TAG                 IMAGE ID            CREATED             SIZE
thiagoavadore/hdfs-yarn-spark-hive                       latest              e8db1d0114d0        3 days ago          1.52GB
ubuntu                                                   trusty              a35e70164dfb        7 weeks ago         222MB
...
```

Now we have an image and we can use the famous `docker run` command to run (*you don't say?!*) a Docker **container** based on the **Ubuntu** image.

```bash
$ docker run ubuntu

$
```
Huh? I didn't get anything on my terminal... bug! Fail! Chaos! You suck!

Wait, wait... this is not a fail! We need to see what happen under the hood here - a lot, trust me! When you ask for Docker to `run` something, the client will look for the image locally (we just pulled it!), lod that container and run a command.
<br> Since we only ordered `docker run ubuntu`, we didn't provide any command. Thus, it just ran the command `____` (empty) and exited. 
<br>*TL;DR; booted up the container, ran empty command and exited*.

Now let's try something extra. 

```bash
$ docker run ubuntu echo $PATH
/usr/local/opt/python@2/libexec/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/go/bin:/usr/local/opt/python@2/libexec/bin
```
Yay! Output!! The Docker client ran the `echo` command in our ubuntu container and then exited it. In milisseconds you got it back your answer! Can you imagine doing the same on a VM?

Another important commands is the `docker ps`. It shows you all containers that are currently running.

```bash
$ docker ps

CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```

Well... no containers running NOW. A nice flag to add is `-a` and that let's you see all containers we ran.

```bash
$ docker ps -a

CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                           PORTS                      NAMES
eaaed95e08a1        ubuntu              "echo /usr/local/opt…"   53 seconds ago       Exited (0) 55 seconds ago                                  frosty_kowalevski
...
```

Notice the `STATUS` column and that it outputs that container has exited.

You might be thinking that this doesn't sound very useful right? You execute one command your command dies? Yes, containers are supposed to be ephemeral... however you can do more interactive sessions with containers. 

```bash
$ docker run -it ubuntu sh

/# ls
bin  boot  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var

/ # uptime
18:23:45 up  2:29,  0 users,  load average: 0.32, 0.44, 0.48
```

The `-it` flags attaches to an interactive tty in the container. Yup, you are in a shell on that script... like you are SSH'ing into a Ubuntu machine. Test it around and play with other commands you know.

Now you know how to look for images in the Docker Hub registry, how to pull images and basic use some tags, how to run containers, how to run containers with specific commands and how to interactively work in a container. It is wise to understand now how to **delete containers**. 
<br> We already saw that `docker ps -a` will show running containers and ones you exited, right? Every time you do a docker run, it will spawn a new container and that may end up consuming a lot of your disk space. To remove containers you do something similar as to removing a file in Unix-based systems, `rm`.

```bash
$ docker rm _some_container_id another_container_id
```

And if you think of Images as VBox files, you can also imagine that images may consume a lot of space. You can also remove them with `rmi`.

```bash
$ docker rmi _some_image_id another_image_id
```

<a id="docker-applications"></a>
## 2. Docker Applications

<a id="static-site"></a>
### 2.1 Static Sites
Let's avoid start running a marathon... to understand how Docker can help you while building an application we will start with the simplest thing: a static website. We're going to pull a Docker image from my Docker Hub, run the container and see how easy it is to run it as a webserver.

The image that we are going to use is a single-page website that I've already created for this club-day and hosted on the [registry](https://hub.docker.com/r/thiagoavadore/nginx-static/) - `thiagoavadore/nginx-static`. A direct `docker run` will check for the image locally, and if not there, it will pull.

```bash
$ docker run thiagoavadore/nginx-static
```

Well, it succeeds, right? Can you do a `docker ps`? What? Nothing is running... hummm... maybe it is time to know more about the daemon flag.

Images like these one are supposed to be running on the background, like a daemon style, a service. Docker has a flag for it, `-d`, for dettached. But before we just do that, let's think of one thing. NGINX by default exposes port 80. Docker has another flag, `-p` (for port), where you can do a port map. It is better to understand this in action, like he command.

```bash
$ docker run -d -p 9898:80 thiagoavadore/nginx-static
```

This will run the NGINX image on the background (`-d`) and map the port 80 of the container to port 9898 of the host where docker is running (`-p 9898:80`). On this case, the localhost port 9898 will have the content of our site! Go to [http://localhost:9898] to check! 

To stop a daemon/detached container, run `docker stop` by giving the container ID. 

<a id="docker-images"></a>
### 2.2 Docker Images

We've looked at images, know how to find and pull them. Now let's go deeper and see how to build our own image.

Docker images are the basis of containers. In the previous example, we **pulled** the *Ubuntu* image from the registry and asked the Docker client to run a container **based** on that image. To see the list of images that are available locally, use the `docker images` command.

```bash
$ docker images
```

The result of the command has some interesting information. The column `TAG` refers to a particular snapshot of the image and the `IMAGE ID` is the corresponding unique identifier for that image.

Like I said before, you can think of images registries as a git repository. Thus you can version it and have different releases/version. That is where tags come in... If you don't provide a specific version number, the client defaults to `latest`. For example, you can pull a specific version of `ubuntu` image

```bash
$ docker pull ubuntu:14.04
```

To get a new Docker image you can either get it from the millions available on public registries (such as the Docker Hub) or create your own. You can also search for images directly from the command line using `docker search`.

It is importan to distinguish base and child images.

- **Base images** are images that have no parent image, usually images with an OS like ubuntu or debian.

- **Child images** are images that build on base images and add additional functionality.

Then there are official and user images, which can be both base and child images.

- **Official images** are images that are officially maintained and supported by the folks at Docker. These are typically one word long, so no need for the `user/image-name` (`python`, `ubuntu`, `debian` and `hello-world` images are base images)

- **User images** are images created and shared by users. They build on base images and add additional functionality. Typically, these are formatted as `user/image-name`.

<a id="our-image"></a>
### 2.3 A First Image

Let's create an image that sandboxes a simple [Flask](http://flask.pocoo.org) application. I have already created an app for this that displays a random picture from someone from the LINKIT.

```
$ git clone bitbucket
$ cd random-pic
```

The next step now is to create an image with this web app. As mentioned above, all user images are based off of a base image. Since our application is written in Python, the base image we're going to use will be [Python 3](https://hub.docker.com/_/python/). More specifically, we are going to use the `python:3-onbuild` version of the python image.

What's the `onbuild` version you might ask?

> These images include multiple ONBUILD triggers, which should be all you need to bootstrap most applications. The build will COPY a `requirements.txt` file, RUN `pip install` on said file, and then copy the current directory into `/usr/src/app`.

In other words, the `onbuild` version of the image includes helpers that automate the boring parts of getting an app running. Rather than doing these tasks manually (or scripting these tasks), these images do that work for you. We now have all the ingredients to create our own image - a functioning web app and a base image. How are we going to do that? The answer is - using a **Dockerfile**.

A [Dockerfile](https://docs.docker.com/engine/reference/builder/) is a simple text-file that contains a list of commands that the Docker client calls while creating an image. It's a simple way to automate the image creation process. The best part is that the [commands](https://docs.docker.com/engine/reference/builder/#from) you write in a Dockerfile are *almost* identical to their equivalent Linux commands. This means you don't really have to learn new syntax to create your own dockerfiles.

The application directory does contain a Dockerfile but since we're doing this for the first time, we'll create one from scratch. To start, create a new blank file in our favorite text-editor and save it in the **same** folder as the flask app by the name of `Dockerfile`.

We start with specifying our base image. Use the `FROM` keyword to do that -

```bash
FROM python:3-onbuild
```

The next step usually is to write the commands of copying the files and installing the dependencies. Luckily for us, the `onbuild` version of the image takes care of that. The next thing we need to the specify is the port number that needs to be exposed. Since our flask app is running on port `5000`, that's what we'll indicate.

```bash
EXPOSE 5000
```

The last step is to write the command for running the application, which is simply - `python ./app.py`. We use the [CMD](https://docs.docker.com/engine/reference/builder/#cmd) command to do that -

```bash
CMD ["python", "./app.py"]
```

The primary purpose of `CMD` is to tell the container which command it should run when it is started. With that, our `Dockerfile` is now ready. This is how it looks like -

```bash
# our base image
FROM python:3-onbuild

# specify the port number the container should expose
EXPOSE 5000

# run the application
CMD ["python", "./app.py"]
```

Now that we have our `Dockerfile`, we can build our image. The `docker build` command does the heavy-lifting of creating a Docker image from a `Dockerfile`.

The section below shows you the output of running the same. Before you run the command yourself (don't forget the period), make sure to replace my username with yours. This username should be the same one you created when you registered on [Docker hub](https://hub.docker.com). If you haven't done that yet, please go ahead and create an account. The `docker build` command is quite simple - it takes an optional tag name with `-t` and a location of the directory containing the `Dockerfile`.

```bash
$ docker build -t prakhar1989/catnip .
Sending build context to Docker daemon 8.704 kB
Step 1 : FROM python:3-onbuild
# Executing 3 build triggers...
Step 1 : COPY requirements.txt /usr/src/app/
 ---> Using cache
Step 1 : RUN pip install --no-cache-dir -r requirements.txt
 ---> Using cache
Step 1 : COPY . /usr/src/app
 ---> 1d61f639ef9e
Removing intermediate container 4de6ddf5528c
Step 2 : EXPOSE 5000
 ---> Running in 12cfcf6d67ee
 ---> f423c2f179d1
Removing intermediate container 12cfcf6d67ee
Step 3 : CMD python ./app.py
 ---> Running in f01401a5ace9
 ---> 13e87ed1fbc2
Removing intermediate container f01401a5ace9
Successfully built 13e87ed1fbc2
```

If you don't have the `python:3-onbuild` image, the client will first pull the image and then create your image. Hence, your output from running the command will look different from mine. Look carefully and you'll notice that the on-build triggers were executed correctly. If everything went well, your image should be ready! Run `docker images` and see if your image shows.

The last step in this section is to run the image and see if it actually works (replacing my username with yours).

```bash
$ docker run -p 8888:5000 thiagoavadore/random-pic
```

The command we just ran used port 5000 for the server inside the container, and exposed this externally on port 8888. Head over to the URL with port 8888, where your app should be live.

Yay! We learned how to create a Docker image!!

<a id="closer-to-real-life"></a>
### 3. Closer to real-life

As you can imagine, what we deployed before is not something used a lot. It is an stateless application without any distinction on backend and fronted. On the real world, we are usually facing at least 3 tiers: backend, frontend and a state manager (databases are the usual). So now we are going to see how that is handled on Docker. The app that we're going to Dockerize is a simple voting app, where we can choose between Cats or Dogs with the following architecture:

![Architecture diagram](example-voting-app/architecture.png)

* A Python Flask webapp which lets you vote between two options
* A Redis queue which collects new votes
* A .NET worker which consumes votes and stores them in…
* A Postgres database backed by a Docker volume
* A Node.js webapp which shows the results of the voting in real time

This is a very good example of the power of Docker. I am using 5 different components that complement each other: a Redis KV to handle queues, PostgreSQL to manage state and 3 languages to write my backend and frontend (Python + Node + .NET).

Great, so we need five containers. And as you can imagine, PostgreSQL and Redis image already exist out-of-the-box with great support on DockerHub.

```bash
$ docker search redis

NAME                              DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
redis                                Redis is an open source key-value store that…   5084                [OK]
bitnami/redis                        Bitnami Redis Docker Image                      73                                      [OK]
...
```

As expected, there is an official image for Redis. To get it running, we can simply use `docker run` and have a single-node Redis container running locally within no time.

```bash
$ docker run --name redis-container -d -p 12345:6379 redis

$ echo PING | nc localhost 12345
+PONG
```

You can see that we learned how to deploy a Redis base image from scratch... but there are 5 containers to create on our case! A PostgreSQL image is similar to Redis, because there is an official image with very good documentation on the DockerHub.

The other 3 images (voting frontend, backend, result frontend) need each one an image. Let's check them...

```bash
$ cd example-voting-app/result

$ cd example-voting-app/vote

$ cd example-voting-app/worker
```
Let's get over these images now...

After looking these images, let's spawn the `results fronted`. Check out how you have issues... why? Because there is no `db` to connect... where is our PostgreSQL?

How do we make containers aware of other containers running around? How do we orchestrate it?


<a id="docker-network"></a>
### 3.1 Docker Network
Now is a good time to start our exploration of networking in Docker. When docker is installed, it creates three networks automatically.

```
$ docker network ls

NETWORK ID          NAME                          DRIVER              SCOPE
fff091fb03c2        bridge                        bridge              local
a1ee3147f5ab        host                          host                local
2c51b29e1c24        none                          null                local
```
The **bridge** network is the network in which containers are run by default. Thus, the Redis container is running here. Let's check that.

```json
$ docker network inspect bridge
[
    {
        "Name": "bridge",
        "Id": "fff091fb03c2c6149f7a708866f1d65dc8e2beb03f27304a7bb72b7e4f6f65f6",
        "Created": "2018-04-27T07:48:46.032749267Z",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": [
                {
                    "Subnet": "172.17.0.0/16",
                    "Gateway": "172.17.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {
            "e2a9f92183ea7519ab0961ff6c7086a2bf6a97224d0cd537a411148598f564cc": {
                "Name": "redis-container",
                "EndpointID": "5906a4bc30d9d8d653f978f4f2fcb3fbfdb3c890190d8ef8a347772376efd4b3",
                "MacAddress": "02:42:ac:11:00:02",
                "IPv4Address": "172.17.0.2/16",
                "IPv6Address": ""
            }
        },
        "Options": {
            "com.docker.network.bridge.default_bridge": "true",
            "com.docker.network.bridge.enable_icc": "true",
            "com.docker.network.bridge.enable_ip_masquerade": "true",
            "com.docker.network.bridge.host_binding_ipv4": "0.0.0.0",
            "com.docker.network.bridge.name": "docker0",
            "com.docker.network.driver.mtu": "1500"
        },
        "Labels": {}
    }
]
```

Hummmm.... so there is a container listed under the `Containers` section in the output. And it has an IPv4 address! So if you are building an application (like we do) that needs to talk with the Redis containers we could hack or way around that.

```bash
$ docker run -it python bash

/# apt-get update
/# apt-get install -yqq netcat
/# echo PING | nc 172.17.0.2 6379
+PONG
```

Nice! We have figured out a way to make the containers talk to each other, but it is not very scalable...

1. We would need to add an entry into the `/etc/hosts` file of the container so that it knows the Redis hostname pointing to `172.17.0.2`. Containers should be disposable... so if the IP keeps changing, manually editing this entry would be quite tedious.

2. Since the *bridge* network is shared by every container by default, this method is **not secure**.

The good news that Docker has a great solution to this problem. It allows us to define our own networks while keeping them isolated. It also tackles the `/etc/hosts` problem and we'll quickly see how.

Let's first go ahead and create our own network.
```bash
$ docker network create voting
c3106a2158805d819205dfbf411f7bd96e8700d134f61909edcb32d9ed6431f6

$ docker network ls
```

For the Ops/curious people: the `network create` command creates a new *bridge* network, which is OK for our case. There are other kinds of networks that you can create, and you are encouraged to read about them in the official [docs](https://docs.docker.com/engine/userguide/networking/dockernetworks/).

Now that we have a network, we can launch our containers inside this network using the `--net` flag.

```json

$ docker run --name redis-container -d -p 12345:6379 --net voting redis

$ docker network inspect voting
[
    {
        "Name": "voting",
        "Id": "c3106a2158805d819205dfbf411f7bd96e8700d134f61909edcb32d9ed6431f6",
        "Created": "2018-04-28T20:31:10.0616956Z",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": {},
            "Config": [
                {
                    "Subnet": "172.21.0.0/16",
                    "Gateway": "172.21.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {
            "0af1cd0810b15273ad0500ac93906d6785abd41859f5612c8aac6e0037b4a052": {
                "Name": "redis-container",
                "EndpointID": "9d6824de07521976943ac8411250fab8db7c85e7a2963ac438d2cc33b6856f6a",
                "MacAddress": "02:42:ac:15:00:02",
                "IPv4Address": "172.21.0.2/16",
                "IPv6Address": ""
            }
        },
        "Options": {},
        "Labels": {}
    }
]
```

Now let's retry the `ping-pong` from a python container on the same network.

```bash
$ docker run -it --net voting python bash

/# apt-get update
/# apt-get install -yqq netcat
/# echo PING | nc redis-container 6379
+PONG
```

Feels like magic! Docker made the correct host file entry in `/etc/hosts` which means that `redis-container:6379` correctly resolves to the IP address of the Redis container.

Still, this is OK and involves a bit of `bash` scripting... but there is something even better!


<a id="docker-compose"></a>
### 3.2 Docker Compose

Till now we've spent all our time exploring the Docker client. In the Docker ecosystem, however, there are a bunch of other open-source tools which play very nicely with Docker. A few of them are -

1. [Docker Machine](https://docs.docker.com/machine/) - Create Docker hosts on your computer, on cloud providers, and inside your own data center
2. [Docker Compose](https://docs.docker.com/compose/) - A tool for defining and running multi-container Docker applications.
3. [Docker Swarm](https://docs.docker.com/swarm/) - A native clustering solution for Docker

In this section, we are going to look at one of these tools, Docker Compose, and see how it can make dealing with multi-container apps easier.

The background story of Docker Compose is quite interesting. Roughly two years ago, a company called OrchardUp launched a tool called Fig. The idea behind Fig was to make isolated development environments work with Docker. The project was very well received on [Hacker News](https://news.ycombinator.com/item?id=7132044) - I oddly remember reading about it but didn't quite get the hang of it.

The [first comment](https://news.ycombinator.com/item?id=7133449) on the forum actually does a good job of explaining what Fig is all about.

> So really at this point, that's what Docker is about: running processes. Now Docker offers a quite rich API to run the processes: shared volumes (directories) between containers (i.e. running images), forward port from the host to the container, display logs, and so on.  But that's it: Docker as of now, remains at the process level.

> While it provides options to orchestrate multiple containers to create a single "app", it doesn't address the managemement of such group of containers as a single entity.
> And that's where tools such as Fig come in: talking about a group of containers as a single entity. Think "run an app" (i.e. "run an orchestrated cluster of containers") instead of "run a container".

It turns out that a lot of people using docker agree with this sentiment. Slowly and steadily as Fig became popular, Docker Inc. took notice, acquired the company and re-branded Fig as Docker Compose.

So what is *Compose* used for? Compose is a tool that is used for defining and running multi-container Docker apps in an easy way. It provides a configuration file called `docker-compose.yml` that can be used to bring up an application and the suite of services it depends on with just one command.

Let's see if we can create a `docker-compose.yml` file for our voting app and evaluate whether Docker Compose lives up to its promise.

If you're running Windows or Mac, Docker Compose is already installed as it comes in the Docker Toolbox. Linux users can easily get their hands on Docker Compose by following the [instructions](https://docs.docker.com/compose/install/) on the docs. Since Compose is written in Python, you can also simply do `pip install docker-compose`. Test your installation with -
```
$ docker-compose version
docker-compose version 1.21.0, build 5920eb0
docker-py version: 3.2.1
CPython version: 3.6.4
OpenSSL version: OpenSSL 1.0.2o  27 Mar 2018
```

Now that we have it installed, we can jump on the next step i.e. the Docker Compose file `docker-compose.yml` inside our `example-voting-app`.

```bash
$ cd example-voting-app

$ docker-compose up
...
```

Head over to the IP to see your app live. That was amazing wasn't it? Just few lines of configuration and we have five Docker containers running successfully in unison. To avoid the verbose outputs, you can run `docker-compose` in detached mode.

```bash
$ docker-compose up -d
...
```

Unsurprisingly, we can see all the containers running successfully. Where do the names come from? Those were created automatically by Compose. But does *Compose* also create the network automatically? Good question! Let's find out.

First off, let us stop the services from running. We can always bring them back up in just one command.

```
$ docker-compose stop
Stopping example-voting-app_worker_1 ... done
Stopping example-voting-app_result_1 ... done
Stopping example-voting-app_vote_1   ... done
Stopping redis                       ... done
Stopping db                          ... done
```

While we're are at it, we'll also remove the `voting` network that we created last time. This should not be required since *Compose* would automatically manage this for us.

```bash
$ docker network rm voting
$ docker network ls
```

Great! Now that we have a clean slate, let's re-run our services and see if *Compose* does it's magic.

```bash
$ docker-compose up -d

$ docker network ls
```
You can see that compose went ahead and created two new networks  and attached to the correct service in that network so that they are discoverable to the other. Let's see if that information resides in `/etc/hosts`.

```bash
$ docker ps

$ docker exec -it $container_id bash

/# cat /etc/hosts
```

What, wait?! Fail! ow is our app working? Let's see if can ping this hostname -

```bash

$ docker exec -it $voting_id ash
/# echo PING | nc redis 6379
+PONG
```

Voila! That works. So somehow, this container is magically able to ping `redis` hostname. Since Docker 1.10 a new networking system was added that does service discovery using a DNS server. If you're interested, you can read more about the [proposal](https://github.com/docker/libnetwork/issues/767) and [release notes](https://blog.docker.com/2016/02/docker-1-10/).

That concludes our tour of Docker Compose. With Docker Compose, you can also pause your services, run a one-off command on a container and even scale the number of containers. I also recommend you checkout a few other [use-cases](https://docs.docker.com/compose/overview/#common-use-cases) of Docker compose. Hopefully I was able to show you how easy it is to manage multi-container environments with Compose. 

<a id="next-steps"></a>
## 4. Next Steps
And that's a wrap! I hope it was enjoyable... You learnt how to setup Docker, run your own containers, play with static and dynamic websites and most importantly got hands on experience with deploying your applications! I hope that finishing this tutorial makes you more confident in your abilities to deal with servers. When you have an idea of building your next app, you can be sure that you'll be able to get it in front of people with minimal effort.

And now we move on to something else: Kubernetes and the orchestrators!

**Additional Resources**

- [Awesome Docker](https://github.com/veggiemonk/awesome-docker)
- [Hello Docker Workshop](http://docker.atbaker.me/)
- [Building a microservice with Node.js and Docker](https://www.youtube.com/watch?v=PJ95WY2DqXo)
- [Why Docker](https://blog.codeship.com/why-docker/)
- [Docker Weekly](https://www.docker.com/newsletter-subscription) and [archives](https://blog.docker.com/docker-weekly-archives/)

**Troubles/Feedback**

Send in your thoughts, troubles and feedback directly to [me](mailto:thiago.de.faria@linkit.nl).