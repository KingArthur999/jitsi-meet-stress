# Jitsi Meet Stress Test (Selenium)

This project is used to stress test a Jitsi Meet deployment using
headless Chrome + Selenium.

## Features

- Headless Chrome (fake media devices)
- Batch startup to avoid fork storm
- Dockerized (one-command start)
- Suitable for multi-container horizontal scaling

## Requirements

- Docker / Podman
- >= 16 CPU cores recommended
- >= 32GB RAM recommended

## Build Image

```bash
docker build -t jitsi-meet-stress .

## Docker Run
docker run --rm \
  --shm-size=4g \
  jitsi-meet-stress \
  --room test1 \
  --users 50 \
  --duration 3600

