#!/bin/bash
# install.sh - One-and-done script to setup weightgurus auto-start service
# Run with `sudo bash install.sh`

set -e  # Exit on any error

echo "Setting up Weightgurus auto-start service..."

# Check if we're in the right directory
if [ ! -f "src/app.py" ]; then
    echo "Error: This script must be run from the weightgurus project directory"
    echo "Please cd to ~/Projects/weightgurus and run this script again"
    exit 1
fi

# Create the startup script
echo "Creating startup script..."
cat > startup_weightgurus.sh << 'EOF'
#!/bin/bash
# Wait for desktop environment to be ready
sleep 60
# Run the existing script
cd ~/Projects/weightgurus && ./run.sh
EOF

# Make startup script executable
chmod +x startup_weightgurus.sh

# Create the systemd service file
echo "Creating systemd service..."
sudo tee /etc/systemd/system/weightgurus.service > /dev/null << EOF
[Unit]
Description=Weightgurus Application
After=graphical-session.target
Wants=graphical-session.target

[Service]
Type=forking
User=dev
Group=dev
WorkingDirectory=/home/dev/Projects/weightgurus
Environment=DISPLAY=:0
ExecStart=/home/dev/Projects/weightgurus/startup_weightgurus.sh
Restart=on-failure
RestartSec=5

[Install]
WantedBy=graphical-session.target
EOF

# Enable and start the service
echo "Enabling and starting the service..."
sudo systemctl daemon-reload
sudo systemctl enable weightgurus.service

echo ""
echo "✅ Installation complete!"
echo ""
echo "📋 What was installed:"
echo "   • weightgurus.service (systemd service)"
echo "   • run.sh (made executable - using your existing script)"
echo ""
echo "🚀 Usage:"
echo "   • Manual start: ./run.sh (test with tmux a -t weightgurus)"
echo "   • Auto-start: Enabled (will start on next boot)"
echo "   • Stop service: sudo systemctl stop weightgurus.service"
echo "   • Check status: sudo systemctl status weightgurus.service"
echo ""
echo "🔄 To test auto-start now (optional):"
echo "   sudo systemctl start weightgurus.service"
echo ""
echo "⚠️  Note: Auto-start will begin working after your next reboot"
