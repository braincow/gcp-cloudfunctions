def ps2bq(event, context):
    from google.cloud import bigquery
    import base64
    import os
    import json
    import sys

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

    # stream the data into bq dataset.table
    table_id = os.environ.get("TABLE_ID")
    if not table_id or table_id == "":
        print("TABLE_ID environment variable cannot be empty",
            file=sys.stderr)
        return

    bq = bigquery.Client()
    errors = bq.insert_rows_json(
        table_id, payload, row_ids=[None] * len(payload))
    if len(errors) == 0:
        if debug_enabled:
            print("Data inserted succesfully.")
    else:
        print("Errors while inserting: {}".format(errors),
            file=sys.stderr)
        return

# eof