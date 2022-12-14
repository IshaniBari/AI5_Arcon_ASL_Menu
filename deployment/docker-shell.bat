SET IMAGE_NAME="arcon-app-deployment"
SET GCP_PROJECT="My First Project"
SET GCP_ZONE="asia-south1-c"
SET GOOGLE_APPLICATION_CREDENTIALS=/secrets/deployment.json
docker build -t %IMAGE_NAME% -f Dockerfile .
cd ..
docker run --rm --name %IMAGE_NAME% -ti ^
           -v /var/run/docker.sock:/var/run/docker.sock ^
           --mount type=bind,source="%cd%\deployment",target=/app ^
           --mount type=bind,source="%cd%\secrets",target=/secrets ^
           --mount type=bind,source="C:\Users\divns\.ssh",target=/home/app/.ssh ^
           --mount type=bind,source="%cd%\api-service",target=/api-service ^
           --mount type=bind,source="%cd%\frontend-react",target=/frontend-react ^
           -e GOOGLE_APPLICATION_CREDENTIALS="%GOOGLE_APPLICATION_CREDENTIALS%" ^
           -e GCP_PROJECT=%GCP_PROJECT% ^
           -e GCP_ZONE=%GCP_ZONE% %IMAGE_NAME%
