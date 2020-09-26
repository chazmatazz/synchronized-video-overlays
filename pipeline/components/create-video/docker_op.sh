#!/bin/bash

rm -rf /tmp/*
docker-compose -f docker-compose.op.yml up --build