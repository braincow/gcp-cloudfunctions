def ps2bq(event, context):
    from google.cloud import iot_v1
    import sys
    import os
    import json

    # check if debug is enabled or not
    debug_enabled = False
    if os.environ.get("DEBUG", "false") != "false":
        debug_enabled = True

    if debug_enabled:
        print(event)
        print(context)

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
    command = json.dumps({ "command": "reset" }).encode()
    client.send_command_to_device(gateway, command)

    print("'{}' was issued a RESET command through IoT Core".format(
        os.environ.get("GATEWAY")
    ))

# eof
