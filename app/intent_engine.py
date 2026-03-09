# app/intent_engine.py

from app.prometheus_client import query_prometheus
from app.config import SERVER_OS


LINUX_CPU = '100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)'
LINUX_MEMORY = '(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100'
LINUX_DISK = '100 - (node_filesystem_avail_bytes{fstype!="tmpfs"} / node_filesystem_size_bytes{fstype!="tmpfs"}) * 100'


WINDOWS_CPU = '100 - (avg(rate(windows_cpu_time_total{mode="idle"}[5m])) * 100)'
WINDOWS_MEMORY = '(1 - (windows_memory_available_bytes / windows_memory_physical_total_bytes)) * 100'
WINDOWS_DISK = '100 - (windows_logical_disk_free_bytes / windows_logical_disk_size_bytes) * 100'


def process_intent(text: str):

    text = text.lower()

    server = None
    metric = None

    if "dev" in text:
        server = "DEV-SERVER"
    elif "qa" in text:
        server = "QA-SERVER"
    elif "uat" in text:
        server = "UAT-SERVER"
    elif "prod" in text:
        server = "PROD-SERVER"

    if "cpu" in text:
        metric = "cpu"
    elif "memory" in text or "ram" in text:
        metric = "memory"
    elif "disk" in text:
        metric = "disk"

    if not server:
        return {"message": "Please specify DEV, QA, UAT, or PROD server.",
                "cpu": None, "memory": None, "disk": None}

    if not metric:
        return {"message": "Please ask about CPU, Memory, or Disk.",
                "cpu": None, "memory": None, "disk": None}

    os_type = SERVER_OS.get(server)

    print(f"\n[INFO] Server: {server}")
    print(f"[INFO] OS: {os_type}")

    if os_type == "linux":
        cpu_query = LINUX_CPU
        mem_query = LINUX_MEMORY
        disk_query = LINUX_DISK

    else:
        cpu_query = WINDOWS_CPU
        mem_query = WINDOWS_MEMORY
        disk_query = WINDOWS_DISK

    cpu = query_prometheus(cpu_query, server)
    memory = query_prometheus(mem_query, server)
    disk = query_prometheus(disk_query, server)

    if metric == "cpu":
        message = f"{server} CPU usage is {cpu}%"
    elif metric == "memory":
        message = f"{server} Memory usage is {memory}%"
    else:
        message = f"{server} Disk usage is {disk}%"

    return {
        "message": message,
        "cpu": cpu,
        "memory": memory,
        "disk": disk
    }