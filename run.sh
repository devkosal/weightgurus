#!/bin/bash
# Make executable with: chmod +x ~/Projects/weightsgurus/run_weightsgurus.sh

#!/bin/bash
cd ~/Projects/weightsgurus
source venv/bin/activate

# Start the app in tmux in the background
tmux new-session -d -s weightsgurus 'python src/app.py --port 5000'

# Wait a moment for the server to start
sleep 3

# Open Firefox in fullscreen
DISPLAY=:0 firefox --new-window http://localhost:5000 &

# Wait for Firefox to load, then make it fullscreen
sleep 5
DISPLAY=:0 xdotool search --name "Mozilla Firefox" windowactivate key F11

echo "WeightsGurus is now running!"
echo "To stop: tmux kill-session -t weightsgurus"
