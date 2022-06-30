#command to build and submit the application

gcloud builds submit --tag gcr.io/streamlit-app-354907/streamlit-app  --project=streamlit-app-354907

#deploy

gcloud run deploy --image gcr.io/streamlit-app-354907/streamlit-app --platform managed  --project=streamlit-app-354907 --allow-unauthenticated
