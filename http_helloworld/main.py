def http_helloworld(request):
    from flask import jsonify
    import os

    # check if debug is enabled or not
    debug_enabled = False
    if os.environ.get("DEBUG", "false") != "false":
        debug_enabled = True

    if debug_enabled:
        print(request)

    return jsonify({"message": "Hello World!"})

# eof