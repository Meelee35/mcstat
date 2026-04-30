def api_url(host: str, port: int) -> str:
    return f"https://api.mcstatus.io/v2/status/java/{host}:{port}"