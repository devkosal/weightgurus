#!/bin/bash
# install.sh - Safe cron installer that avoids duplicates

set -e
echo "Setting up Weightgurus auto-start..."

CRON_JOB="@reboot sleep 60 && cd ~/Projects/weightgurus && ./run.sh"

# Check if the job already exists
if crontab -l 2>/dev/null | grep -q "weightgurus"; then
    echo "⚠️  Weightgurus cron job already exists. Skipping..."
else
    # Add the new cron job
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "✅ Cron job added successfully!"
fi

echo "Current cron jobs:"
crontab -l
