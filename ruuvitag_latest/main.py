def ruuvitag_latest(request):
    from google.cloud import bigquery
    from flask import escape, jsonify
    import os
    import sys

    # check if debug is enabled or not
    debug_enabled = False
    if os.environ.get("DEBUG", "false") != "false":
        debug_enabled = True

    if debug_enabled:
        print(request)

    # read latest values for each tag from bigquery
    table_id = os.environ.get("TABLE_ID")
    if not table_id or table_id == "":
        raise ValueError("TABLE_ID environment variable cannot be empty")

    bq = bigquery.Client()

    latest_query = """
SELECT
  agg.table.*
FROM (
  SELECT
    address,
    ARRAY_AGG(STRUCT(table)
    ORDER BY
      timestamp DESC)[SAFE_OFFSET(0)] agg
  FROM
    `ruuvitag.data` table
  WHERE timestamp > TIMESTAMP_ADD(CURRENT_TIMESTAMP(), INTERVAL -1 MINUTE)
  GROUP BY
    address);
    """

    query_job = bq.query(latest_query)
    records = [dict(row) for row in query_job]

    if debug_enabled:
        print(records)

    return jsonify(records)

# eof