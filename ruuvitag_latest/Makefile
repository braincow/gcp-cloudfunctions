all: none
none:
	@echo Nothing to see here! Go away!

deploy:
	gcloud --quiet functions deploy ruuvitag_latest \
		--source .\
		--region europe-west1 \
		--runtime python38 \
		--trigger-http \
		--env-vars-file env.yaml \
		--memory 256MB

delete:
	gcloud functions delete ruuvitag_latest --region europe-west1 

logs:
	gcloud functions logs read ruuvitag_latest --region europe-west1 

call:
	curl -H "Authorization: Bearer $(shell gcloud auth print-identity-token)" \
		$(shell gcloud functions describe ruuvitag_latest --region europe-west1 --format json |jq .httpsTrigger.url) |jq

