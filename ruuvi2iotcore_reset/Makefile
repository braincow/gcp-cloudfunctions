all: none
none:
	@echo Nothing to see here! Go away!

deploy:
	gcloud functions deploy ruuvi_reset \
		--source .\
		--region europe-west1 \
		--runtime python38 \
		--trigger-topic ruuvi2iotcore \
		--env-vars-file env.yaml \
		--memory 256MB

delete:
	gcloud functions delete ruuvi_reset --region europe-west1 

logs:
	gcloud functions logs read ruuvi_reset --region europe-west1 
