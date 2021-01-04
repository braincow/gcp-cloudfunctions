all: none
none:
	@echo Nothing to see here! Go away!

deploy:
	gcloud --quiet functions deploy http_helloworld \
		--source .\
		--region europe-west1 \
		--runtime python38 \
		--trigger-http \
		--allow-unauthenticated \
		--env-vars-file env.yaml \
		--memory 256MB

delete:
	gcloud functions delete http_helloworld --region europe-west1 

logs:
	gcloud functions logs read http_helloworld --region europe-west1 

call:
	curl $(shell gcloud functions describe http_helloworld --region europe-west1 --format json |jq -r .httpsTrigger.url) |jq
