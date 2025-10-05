# TODO

## 🔧 Local Development
- [ ] Install server deps: `pip install -r server/requirements.txt`
- [ ] Start stack: `docker compose up -d --build`
- [ ] Verify API and db health: `curl http://127.0.0.1:8000/health`

## 🔌 Endpoints
- [ ] `GET /health` returns `{ "ok": true, "db": true }`
- [ ] Add/verify KB endpoints (`/kb/faq`, `/ask`) if needed

## 🐳 Docker (Production) — when ready to deploy
- [ ] Create `docker-compose.prod.yml` with overrides:
  - [ ] Set `APP_ENV=production`
  - [ ] Remove dev volume mounts (read-only image)
  - [ ] Disable `--reload` in server start command
  - [ ] Set `DATABASE_URL` to production DB (do NOT hardcode secrets)
  - [ ] Add `depends_on` healthchecks if needed
- [ ] Configure secrets (Use secrets manager or platform env vars):
  - [ ] Platform env vars (e.g., Render/Railway/Fly/Heroku)
  - [ ] Docker Swarm/Compose `secrets:` or Kubernetes `Secret`
- [ ] Networking:
  - [ ] Expose only the backend port needed externally
  - [ ] Put a reverse proxy (NGINX/Caddy) or platform LB in front
- [ ] Observability:
  - [ ] Keep `/health`  for probes
  - [ ] Add basic logs/stdout collection via platform
- [ ] Run with prod compose:
  - [ ] `docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build`



