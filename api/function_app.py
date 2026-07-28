import azure.functions as func
import json
import datetime

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="hello", methods=["GET", "POST"])
def hello(req: func.HttpRequest) -> func.HttpResponse:
    name = req.params.get("name")
    if not name:
        try:
            body = req.get_json()
            name = body.get("name")
        except ValueError:
            pass
    name = name or "there"

    payload = {
        "message": f"Hello, {name}! This response came from a Python Managed Function.",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    }

    return func.HttpResponse(
        json.dumps(payload),
        mimetype="application/json",
        status_code=200,
    )
