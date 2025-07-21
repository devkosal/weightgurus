#!/bin/bash
# install.sh - Debug version

set -e
echo "Setting up Weightgurus auto-start..."

# sleep for 15 seconds to ensure system is ready e.g. after reboot
CRON_JOB="@reboot sleep 15 && cd ~/Projects/weightgurus && ./run.sh >> /tmp/weightgurus.log 2>&1"

# Check if the job already exists
if crontab -l 2>/dev/null | grep -q "weightgurus"; then
    echo "⚠️  Weightgurus cron job already exists. Skipping..."
else
    echo "Adding cron job: $CRON_JOB"
    chmod +x ~/Projects/weightgurus/run.sh
    # Try to add with error checking
    if (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab - 2>&1; then
        echo "✅ Cron job command executed"
    else
        echo "❌ Cron job command failed"
        exit 1
    fi
fi

echo "Verifying installation..."
echo "Current cron jobs:"
if crontab -l 2>/dev/null; then
    echo "Cron job count: $(crontab -l 2>/dev/null | wc -l)"
else
    echo "No crontab found or cron service issue"
fi

# Additional debugging
echo "Cron service status:"
systemctl is-active cron 2>/dev/null || systemctl is-active crond 2>/dev/null || echo "Cron service not found/running"
