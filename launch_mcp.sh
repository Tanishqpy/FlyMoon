#!/bin/bash

# ====== CONFIG ======
APP_MODULE="main:app"     # Your FastAPI app module path
PORT=8000                 # Local port to run Uvicorn
NGROK_BIN="ngrok"         # Path to ngrok binary if not in PATH

# ====== START FASTAPI ======
echo "🔁 Starting FastAPI on port $PORT..."
uvicorn "$APP_MODULE" --host 0.0.0.0 --port "$PORT" &
UVICORN_PID=$!

# Give uvicorn a second to start
sleep 2

# ====== START NGROK ======
echo "🌍 Starting Ngrok tunnel..."
$NGROK_BIN http "$PORT" > /dev/null &
NGROK_PID=$!

# ====== WAIT FOR NGROK TO INIT ======
sleep 3

# ====== FETCH NGROK PUBLIC URL ======
NGROK_URL=$(curl --silent http://localhost:4040/api/tunnels | grep -Eo 'https://[a-zA-Z0-9\-]+\.ngrok-free\.app')
echo "✅ MCP Server is LIVE at: $NGROK_URL"

# ====== CLEAN EXIT ON CTRL+C ======
trap "echo '🛑 Shutting down...'; kill $UVICORN_PID $NGROK_PID; exit" SIGINT

# Keep script running until Ctrl+C
wait
