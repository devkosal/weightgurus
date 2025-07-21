#!/bin/bash
# uninstall.sh - Remove weightgurus auto-start service

echo "Removing Weightgurus auto-start service..."

# Stop the service if it's running
echo "Stopping service..."
sudo systemctl stop weightgurus.service 2>/dev/null || echo "Service not running"

# Disable the service
echo "Disabling service..."
sudo systemctl disable weightgurus.service 2>/dev/null || echo "Service not enabled"

# Remove the service file
echo "Removing service file..."
sudo rm -f /etc/systemd/system/weightgurus.service

# Reload systemd
echo "Reloading systemd..."
sudo systemctl daemon-reload

echo ""
echo "✅ Uninstall complete!"
echo ""
echo "📋 What was removed:"
echo "   • weightgurus.service (systemd service)"
echo ""
echo "📝 Note: Your run.sh script was left untouched"
