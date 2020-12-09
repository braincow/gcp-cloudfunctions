def ps2bq(event, context):
    from google.cloud import bigquery
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
        raise ValueError("No 'data' field in event")

    # stream the data into bq dataset.table
    table_id = os.environ.get("TABLE_ID")
    if not table_id or table_id == "":
        raise ValueError("TABLE_ID environment variable cannot be empty")

    bq = bigquery.Client()
    errors = bq.insert_rows_json(
        table_id, payload, row_ids=[None] * len(payload))
    if len(errors) == 0:
        if debug_enabled:
            print("Data inserted succesfully.")
    else:
        raise RuntimeError("Errors while inserting data: {}".format(errors))

# eof