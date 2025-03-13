# app/services/sys_stats_service.py
import psutil
import threading
import time
from app.config import db
from datetime import datetime

def get_collection():
    """Get the MongoDB collection for system stats."""
    return db["admin_sys_stats"]

def collect_system_stats():
    """Collect CPU, RAM, and Network utilization stats."""
    return {
        "cpu_usage": psutil.cpu_percent(interval=1),
        "ram_usage": psutil.virtual_memory().percent,
        "network_io": {
            "bytes_sent": psutil.net_io_counters().bytes_sent,
            "bytes_received": psutil.net_io_counters().bytes_recv
        },
        "timestamp": datetime.utcnow()
    }

def store_system_stats():
    """Collect and store system stats in MongoDB every second."""
    while True:
        try:
            collection = get_collection()
            stats = collect_system_stats()
            collection.insert_one(stats)
            print(f"Stored system stats: {stats}")  # Log to console
        except Exception as e:
            print(f"Error storing system stats: {e}")
        time.sleep(1)  # Wait 1 second before collecting again

# Run the stats collection in a background thread
def start_monitoring():
    """Start the system monitoring in a separate thread."""
    thread = threading.Thread(target=store_system_stats, daemon=True)
    thread.start()
