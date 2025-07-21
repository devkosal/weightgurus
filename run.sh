#!/bin/bash

# to have this script run on startup, add it to your crontab

# Start the app in tmux in the background
/usr/bin/tmux new-session -d -s weightgurus 'cd /home/dev/Projects/weightgurus && /home/dev/Projects/weightgurus/venv/bin/python src/app.py --port 5000'

# Wait a moment for the server to start
sleep 3

# Open Firefox in fullscreen
DISPLAY=:0 firefox http://localhost:5000 &

echo "weightgurus is now running!"
echo "To stop: tmux kill-session -t weightgurus"
