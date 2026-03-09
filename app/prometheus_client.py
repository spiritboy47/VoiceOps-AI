# app/prometheus_client.py

import requests
from app.config import SERVER_PROMETHEUS_MAPPING


def query_prometheus(promql: str, server_name: str):

    prom_url = SERVER_PROMETHEUS_MAPPING.get(server_name.upper())

    if not prom_url:
        print(f"[ERROR] Unknown server: {server_name}")
        return None

    try:

        url = f"{prom_url}/api/v1/query"

        print(f"\n[DEBUG] Querying {server_name}")
        print(f"[DEBUG] URL: {url}")
        print(f"[DEBUG] PROMQL: {promql}")

        response = requests.get(
            url,
            params={"query": promql},
            timeout=10
        )

        data = response.json()

        print(f"[DEBUG] Raw Response: {data}")

        result = data["data"]["result"]

        if not result:
            print("[DEBUG] No results returned")
            return None

        value = float(result[0]["value"][1])

        print(f"[DEBUG] Parsed Value: {value}")

        return round(value, 2)

    except Exception as e:
        print("[ERROR] Prometheus query failed:", str(e))
        return None