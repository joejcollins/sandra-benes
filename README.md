# RAG and MCP demo

Running at <https://sandra-benes.onrender.com>.

Docs at <https://joejcollins.github.io/sandra-benes/>.

Start command `gunicorn -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT sandra_benes.fastapi:APP`

## Confirm Elastic

`curl -s http://elasticsearch:9200`

## To Do

- [x] Ping handler
- [x] HTTP ping endpoint
- [x] MCP ping endpoint
- [ ] Prometheus endpoint
- [ ] logging
- [ ] /healthz endpoint for render.com
