#!/bin/bash

echo "===================================="
echo "Backing Up Job Application Data"
echo "===================================="
echo ""

# Create backup folder with timestamp
timestamp=$(date +"%Y%m%d_%H%M%S")
backup_folder="backups/backup_$timestamp"

echo "Creating backup folder: $backup_folder"
mkdir -p "$backup_folder"

# Backup database
echo "Backing up database..."
if cp backend/job_tracker.db "$backup_folder/job_tracker.db" 2>/dev/null; then
    echo "[OK] Database backed up"
else
    echo "[ERROR] Failed to backup database"
fi

# Backup uploads folder
echo "Backing up uploaded files..."
if cp -r backend/uploads "$backup_folder/" 2>/dev/null; then
    echo "[OK] Uploads backed up"
else
    echo "[ERROR] Failed to backup uploads"
fi

echo ""
echo "===================================="
echo "Backup Complete!"
echo "===================================="
echo "Location: $backup_folder"
echo ""

# Show backup size
du -sh "$backup_folder"

echo ""
echo "You can restore by copying files from backup folder"
echo "back to backend/ folder."
echo ""

