def ruuvi2iotcore_reset(event, context):
    from google.cloud import iot_v1
    import sys
    import os
    import json
    import base64

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
        if not isinstance(payload, dict):
            print("Payload is not a dictionary!", file=sys.stderr)
            return
    else:
        print("No data present in the message.", file=sys.stderr)
        return
    
    if payload["incident"]["state"] == "open":
        # https://googleapis.dev/python/cloudiot/latest/index.html
        # connect to IoT core using cloudfunction's runtime service account
        #  privileges
        client = iot_v1.DeviceManagerClient()
        gateway = client.device_path(
            os.environ.get("PROJECT"),
            os.environ.get("REGION"),
            os.environ.get("REGISTRY"),
            os.environ.get("GATEWAY"))

        # this is the command to send to device in case a reset is needed
        command = json.dumps({ "command": "reset" }).encode("utf-8")
        client.send_command_to_device(request={
            "name": gateway,
            "binary_data": command
            })

        print("'{}' was issued a RESET command through IoT Core".format(
            os.environ.get("GATEWAY")
            ))
    elif payload["incident"]["state"] == "closed":
        print("'{}' recovered. Taking no action.".format(
            os.environ.get("GATEWAY")
            ))
    else:
        print("Unknown incident state received.", file=sys.stderr)

# eof
