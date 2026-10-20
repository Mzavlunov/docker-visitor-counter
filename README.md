# Docker Visitor Counter

A tiny local Python website used to demonstrate **Docker image builds, containers, port publishing, Docker Compose, environment variables, container health checks, and persistent named volumes**. The application has no third-party Python dependencies.

## Prerequisites
- Docker Desktop running (Windows, macOS, or Linux), with Docker Compose v2
- A terminal (e.g. PowerShell)
- Git only if publishing to GitHub

## Quick start

```powershell
docker compose up --build -d
docker compose ps
```

Visit http://localhost:5000 and refresh. The counter increases.

## Demonstrate that the volume persists after the container is recreated

1. Open http://localhost:5000 and note the count (e.g. 5).
2. `docker compose down` (removes the container but retains the named volume).
3. `docker compose up -d` (creates a new container from the image).
4. Refresh the page. The counter increases from the saved count rather than restarting at 1.


## Demonstrate environment variables

Change `APP_TITLE` in `compose.yaml`, then run `docker compose up -d --force-recreate` and refresh. The heading changes without modifying `app.py`.

## Other useful commands

```powershell
docker compose ps                 # Check status / health
docker compose logs               # Inspect application logs
docker image ls                   # List locally built images
docker volume ls                  # List volumes
docker compose down               # Stop and remove container/network; keep data
```

## Architecture

`Browser (localhost:5000) -> Docker published port 5000 -> Python app in container -> /data/visits.txt on named Docker volume`

## Assignment evidence

Capture your **own** screenshots of:

1. A browser displaying the working page and its visit count.
2. A PowerShell terminal showing `docker compose up --build -d` and `docker compose ps` with `healthy`.
3. A `docker volume ls` result and/or `docker volume inspect` for your volume.
4. The browser count before `docker compose down`, and after `docker compose up -d` (persistence evidence).
5. Your repository containing `Dockerfile`, `compose.yaml`, and `app.py`.

## Limitations

This is a local learning demo, not a production web service. It uses Python's standard-library `HTTPServer` and a text file, so it is intentionally simple and not designed for concurrent traffic.
