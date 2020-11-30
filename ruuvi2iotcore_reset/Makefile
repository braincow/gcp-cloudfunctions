all: none
none:
	@echo Nothing to see here! Go away!

deploy:
	gcloud functions deploy ruuvi2iotcore_reset \
		--source .\
		--region europe-west1 \
		--runtime python38 \
		--trigger-topic monitor-ruuvi2iotcore \
		--env-vars-file env.yaml \
		--memory 256MB

delete:
	gcloud functions delete ruuvi2iotcore_reset --region europe-west1 

logs:
	gcloud functions logs read ruuvi2iotcore_reset --region europe-west1 
