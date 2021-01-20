def ruuvitags(request):
    from google.cloud import bigquery
    from flask import jsonify, abort, make_response
    import os

    # check if debug is enabled or not
    debug_enabled = False
    if os.environ.get("DEBUG", "false") != "false":
        debug_enabled = True

    if debug_enabled:
        print(request)

    # read all known tags from database
    table_id = os.environ.get("TABLE_ID")
    if not table_id or table_id == "":
        raise ValueError("TABLE_ID environment variable cannot be empty")

    bq = bigquery.Client()

    tags_query = "SELECT * FROM {}".format(table_id)

    query_job = bq.query(tags_query)
    records = [dict(row) for row in query_job]

    if len(records) == 0:
        return abort(make_response(jsonify(
            message="No records returned from database"), 404))

    if debug_enabled:
        print(records)

    return jsonify(records)

# eof