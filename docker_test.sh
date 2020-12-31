#!/usr/bin/env bash

docker run -v `pwd`/samples:/work -v `pwd`/output:/output -it chuy08/sortpics:latest
