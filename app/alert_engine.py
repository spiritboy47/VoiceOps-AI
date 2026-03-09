#======== alert ============
import time

ALERT_CACHE = {}
COOLDOWN = 180  # 3 minutes

from app.prometheus_client import query_prometheus
from app.config import SERVER_OS


LINUX_CPU = '100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)'
LINUX_MEMORY = '(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100'

WINDOWS_CPU = '100 - (avg(rate(windows_cpu_time_total{mode="idle"}[5m])) * 100)'
WINDOWS_MEMORY = '(1 - (windows_memory_available_bytes / windows_memory_physical_total_bytes)) * 100'


SERVERS = ["DEV-SERVER", "QA-SERVER", "UAT-SERVER", "PROD-SERVER"]


# ------------------------------------
# Alert suppression logic (NEW)
# ------------------------------------
def should_send_alert(key):

    now = time.time()

    last_time = ALERT_CACHE.get(key)

    if last_time:
        if (now - last_time) < COOLDOWN:
            return False

    ALERT_CACHE[key] = now
    return True


def check_alerts():

    alerts = []

    for server in SERVERS:

        os_type = SERVER_OS.get(server)

        if os_type == "linux":
            cpu_query = LINUX_CPU
            mem_query = LINUX_MEMORY
        else:
            cpu_query = WINDOWS_CPU
            mem_query = WINDOWS_MEMORY

        cpu = query_prometheus(cpu_query, server)
        memory = query_prometheus(mem_query, server)

        # ---------------- CPU ALERT ----------------
        if cpu and cpu > 80:

            key = f"{server}_cpu"

            if should_send_alert(key):
                alerts.append(f"⚠️ {server} CPU usage is {cpu:.2f}%")

        # -------------- MEMORY ALERT ---------------
        if memory and memory > 85:

            key = f"{server}_memory"

            if should_send_alert(key):
                alerts.append(f"⚠️ {server} Memory usage is {memory:.2f}%")

    return alerts