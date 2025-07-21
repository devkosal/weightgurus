#!/bin/bash
# Make executable with: chmod +x ~/Projects/weightgurus/run.sh

# Start the app in tmux in the background
tmux new-session -d -s weightgurus 'cd ~/Projects/weightgurus && source venv/bin/activate && python src/app.py --port 5000'

# Wait a moment for the server to start
sleep 3

# Open Firefox in fullscreen
DISPLAY=:0 firefox http://localhost:5000 &

echo "weightgurus is now running!"
echo "To stop: tmux kill-session -t weightgurus"
