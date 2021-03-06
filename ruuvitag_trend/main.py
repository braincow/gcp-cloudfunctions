def ruuvitag_trend(request):
    from google.cloud import bigquery
    from flask import jsonify, abort, make_response
    import os
    import numpy

    if "field" not in request.args or "tag" not in request.args \
            or "interval" not in request.args:
        return abort(make_response(jsonify(
            message=("Required field missing from "
                     "request [field, tag, interval]")), 400))
    field = request.args.get("field")
    mins = int(request.args.get("interval")) * -1
    tag = request.args.get("tag")
    if mins >= 0:
        return abort(make_response(jsonify(
            message="Interval must be larger than 0"), 400))

    # check if debug is enabled or not
    debug_enabled = False
    if os.environ.get("DEBUG", "false") != "false":
        debug_enabled = True

    if debug_enabled:
        print(request)
        print(request.args)

    # read latest values for each tag from bigquery
    table_id = os.environ.get("TABLE_ID")
    if not table_id or table_id == "":
        raise ValueError("TABLE_ID environment variable cannot be empty")

    latest_query = """
  SELECT data.address AS address,
    data.timestamp AS timestamp,
    data.data AS data,
    known_tags.name AS name
  FROM {}
  LEFT JOIN ruuvitag.known_tags ON known_tags.address = data.address
  WHERE timestamp >= TIMESTAMP_ADD(CURRENT_TIMESTAMP(),
    INTERVAL @minutes MINUTE) AND known_tags.name = @tagname
  ORDER BY timestamp;
  """.format(table_id)
    job_config = bigquery.QueryJobConfig(
      query_parameters=[
        bigquery.ScalarQueryParameter("minutes", "INT64", mins),
        bigquery.ScalarQueryParameter("tagname", "STRING", tag)
      ]
    )

    bq = bigquery.Client()
    query_job = bq.query(latest_query, job_config=job_config)

    records = [row["data"][field] for row in query_job]
    if len(records) <= 1:
        return abort(make_response(jsonify(
            message="Not enough records to deduce trend from"), 204))
    coeffs = numpy.polyfit([*range(1, len(records) + 1)], records, 1)
    # if the slope is a +ve value --> increasing trend
    # if the slope is a -ve value --> decreasing trend
    # if the slope is a zero value --> No trend
    slope = coeffs[-2]

    retval = {"values": records, "slope": slope, "field": field, "tag": tag}

    if debug_enabled:
        print(retval)

    return jsonify(retval)

# eof
