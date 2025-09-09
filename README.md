# RAG and MCP demo

Running at <https://sandra-benes.onrender.com>.

Start command `gunicorn -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT sandra_benes.fastapi:APP`

## To Do

- [x] Ping handler
- [x] HTTP ping endpoint
- [x] MCP ping endpoint
- [ ] Prometheus endpoint
- [ ] logging
- [ ] /healthz endpoint for render.com
