# Bug Bench

## Benchmark
```
benchmark
|--- PROGRAM1
    `--- VER1
    |    `--- label.json
    |    `--- Dockerfile
    |    `--- build.sh
    `--- VER2
    |    `--- label.json
    |    `--- Dockerfile
    |    `--- build.sh
    ...
```

## Bug Label
See [LABEL.md](LABEL.md).

## Docker
- Base image: `prosyslab/bug-bench-base` in Dockerhub built from [docker/Dockerfile](docker/Dockerfile)
```sh
/
|-- src/
|  `-- PROGRAM/
|  `-- build.sh
|-- smake/
|-- infer/   # shall be mounted
|-- codeql/  # shall be mounted
|-- out/
   `-- smake-out/
   `-- infer-out/
   `-- codeql-db/
```
### Building Docker images
- Building a single image
```
$ bin/build-docker.sh benchmark/[program]/[version]
```
- Building all images including `base`
```
$ bin/build-docker.sh all
```

### How to build with respect to desired target?

```sh
$ $BUILD [ sparrow | infer | codeql ]
```

For example, to build target for Sparrow, run `$BUILD sparrow`. Then, the built target along with either Sparrow or Infer will be located at `/out/*`.

### How to mount `infer` or `codeql`?

```sh
$ docker run -it -v PATH/TO/INFER/DIR/:/infer REPO:TAG
```
or
```sh
$ docker run -it -v PATH/TO/CODEQL/DIR/:/codeql REPO:TAG
```

FYI, look out for `-v` option in `docker run --help`.

### How to upload repository to prosyslab-warehouse?

First, you have to install and authenticate github-cli on your local machine. To install, see [here](https://github.com/cli/cli#installation).

Then, authenticate with your github account:

```sh
$ gh auth login
```

Once auth is done, run the command below to upload source code of the benchmark:

```sh
$ bin/add_repo_to_remote.sh [repo name] [url of tar file]
```

Example
```sh
$ bin/add_repo_to_remote.sh prosyslab-warehouse/shntool-3.0.5 http://shnutils.freeshell.org/shntool/dist/src/shntool-3.0.5.tar.gz
```

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md).
