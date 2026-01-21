def predict_severity_and_category(title: str, description: str) -> tuple[str, str]:
    # This is rule-based logic now, but later it will be replaced by a model.
    text = (title + " " + description).lower()

    if any(k in text for k in ["down", "outage", "crash", "500", "critical"]):
        return "critical", "outage"
    if any(k in text for k in ["slow", "latency", "performance"]):
        return "medium", "performance"
    if any(k in text for k in ["login", "access", "permission", "unauthorized"]):
        return "medium", "access"

    return "low", "request"
