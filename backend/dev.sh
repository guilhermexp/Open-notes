export CORS_ALLOW_ORIGIN="http://localhost:8357"
PORT="${PORT:-36950}"
uvicorn open_webui.main:app --port $PORT --host 0.0.0.0 --forwarded-allow-ips '*' --reload
