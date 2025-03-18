import psutil
import threading
import time
from app.config import db
from datetime import datetime, timedelta

def get_collection():
    """Get the MongoDB collection for system stats."""
    return db["admin_sys_stats"]

def collect_system_stats():
    """Collect CPU, RAM, Network, and Storage utilization stats."""
    return {
        "cpu_usage": psutil.cpu_percent(interval=1),
        "ram_usage": psutil.virtual_memory().percent,
        "network_io": {
            "bytes_sent": psutil.net_io_counters().bytes_sent,
            "bytes_received": psutil.net_io_counters().bytes_recv
        },
        "storage_usage": psutil.disk_usage('/').percent,
        "timestamp": datetime.utcnow()
    }

def delete_old_stats():
    """Delete system stats older than a day."""
    try:
        collection = get_collection()
        cutoff_time = datetime.utcnow() - timedelta(days=1)
        result = collection.delete_many({"timestamp": {"$lt": cutoff_time}})
        if result.deleted_count:
            print(f"Deleted {result.deleted_count} old records.")
    except Exception as e:
        print(f"Error deleting old system stats: {e}")

def delete_if_exceeds_limit():
    """Delete all system stats if the collection has more than 500 documents."""
    try:
        collection = get_collection()
        count = collection.count_documents({})
        if count > 500:
            result = collection.delete_many({})
            print(f"Collection exceeded limit. Deleted all {result.deleted_count} records.")
    except Exception as e:
        print(f"Error checking/deleting system stats: {e}")

def store_system_stats():
    """Collect and store system stats in MongoDB every second."""
    cleanup_interval = 60  # Cleanup every 60 iterations (~1 min)
    count = 0

    while True:
        try:
            collection = get_collection()
            delete_if_exceeds_limit()  # Check and delete if necessary

            stats = collect_system_stats()
            collection.insert_one(stats)
            print(f"Stored system stats: {stats}")

            count += 1
            if count >= cleanup_interval:
                delete_old_stats()
                count = 0  # Reset counter after cleanup
        except Exception as e:
            print(f"Error storing system stats: {e}")
        time.sleep(1)

def start_monitoring():
    """Start the system monitoring in a separate thread."""
    thread = threading.Thread(target=store_system_stats, daemon=True)
    thread.start()
