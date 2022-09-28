# Setup using docker
To build the docker image `cd` to the `docker` folder. In this folder run

```
docker build -t elastixdocker:v0 .
```

To build the docker image. The image is based on a ubuntu 18.04 based image and uses elastix version 5.0.0. 

To run docker container run the following command 
```
docker run -it -v path/to/ElastixExperimentTracker:/home/appuser/elastix elastixdocker:v0
```

where `path/to/ElastixExperimentTracker` is the absolute path to this cloned github repository. The `-v` flag in docker *binds* a volume from the host machine to the docker container. In this case we make it so that the docker can acsess the `ElastixExperimentTracker` on the host machine by binding it to a folder on in the docker container called `~/elastix` (which is equivalent to `/home/user/elastix`). Thus you can modify the code, config and registration parameters on the host machine.

**Note:** All paths specified in the config files are now relative to the `~/elastix` folder in the docker container (which is also the `path/to/ElastixExperimentTracker` on the local machine).

## Adding data
The docker container does **not** have access to the files on the local file system. To access files either need add the files to a bound volume, e.g. putting the in a subfolder of `path/to/ElastixExperimentTracker`, or by binding additional volumes. 

The `-v` flag can be used to bind additional volumes using the syntax `-v absolute/path/in/host/machine:absolute/path/in/container`. Multiple `-v` flags can be used with a single run command. 

```
docker run -it -v path/to/ElastixExperimentTracker:/home/appuser/elastix -v absolute/path/in/host/machine:absolute/path/in/container elastixdocker:v0
```

## Additional flags
 - `--rm` if you want the container to be automatically deleted when excited the `--rm` flag can be used in the `docker run` command. Use this if you are not planning to reconnect to a stopped container by using `docker start <container ID>` followed by `docker attach <container ID>`.