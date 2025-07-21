#!/bin/bash
# uninstall.sh - Remove weightgurus cron job

set -e
echo "Removing Weightgurus auto-start..."

# Check if any weightgurus cron jobs exist
if crontab -l 2>/dev/null | grep -q "weightgurus"; then
    # Remove lines containing "weightgurus" from crontab
    crontab -l 2>/dev/null | grep -v "weightgurus" | crontab -
    echo "✅ Weightgurus cron job removed!"
else
    echo "ℹ️  No weightgurus cron job found."
fi

echo "Current cron jobs:"
crontab -l 2>/dev/null || echo "No cron jobs remaining."
