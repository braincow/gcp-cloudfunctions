def ruuvitag_latest(request):
    from google.cloud import bigquery
    from flask import jsonify, abort, make_response
    import os

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

    tag = request.args.get("tag", "%")

    bq = bigquery.Client()

    latest_query = """
SELECT
  tags.name,
  agg.table.*
FROM (
  SELECT
    table.address as address,
    ARRAY_AGG(STRUCT(table)
    ORDER BY
      timestamp DESC)[SAFE_OFFSET(0)] agg
  FROM
    `{}` table
  WHERE timestamp >= TIMESTAMP_ADD(CURRENT_TIMESTAMP(), INTERVAL -1 MINUTE)
  GROUP BY
    address)
  RIGHT JOIN ruuvitag.known_tags tags
  ON tags.address = agg.table.address
  WHERE tags.name LIKE @tagname;
    """.format(table_id)
    job_config = bigquery.QueryJobConfig(
      query_parameters=[
        bigquery.ScalarQueryParameter("tagname", "STRING", tag)
      ]
    )

    query_job = bq.query(latest_query, job_config=job_config)
    records = [dict(row) for row in query_job]

    if debug_enabled:
        print(records)

    return jsonify(records)

# eof