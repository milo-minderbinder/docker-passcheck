#!/bin/bash

docker build -t mminderbinder/passcheck .
docker run -it --rm -p 127.0.0.1:5000:5000 --name passcheck mminderbinder/passcheck bash
