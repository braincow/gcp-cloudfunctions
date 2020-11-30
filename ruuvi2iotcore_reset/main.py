def ps2bq(event, context):
    from google.cloud import iot_v1
    import sys
    import base64
    import os
    import json

    # check if debug is enabled or not
    debug_enabled = False
    if os.environ.get("DEBUG", "false") != "false":
        debug_enabled = True

    if debug_enabled:
        print(event)
        print(context)

    # pull data out of the event that was sent to our trigger
    payload = None
    if 'data' in event:
        payload = base64.b64decode(event['data']).decode('utf-8')
        if debug_enabled:
            print(payload)
        payload = json.loads(payload)
        if not isinstance(payload, list):
            payload = [payload]
    else:
        print("No data present in the message.", file=sys.stderr)
        return

    # this is the command to send to device in case a reset is needed
    command = json.dumps({ "command": "reset" }).encode()

    # https://googleapis.dev/python/cloudiot/latest/index.html
    client = iot_v1.DeviceManagerClient()
    gateway = client.device_path(
        os.environ.get("PROJECT"),
        os.environ.get("REGION"),
        os.environ.get("REGISTRY"),
        os.environ.get("GATEWAY"))
    
    client.send_command_to_device(gateway, command)

# eof
