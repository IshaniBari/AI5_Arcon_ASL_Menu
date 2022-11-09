REM Define some environment variables
SET IMAGE_NAME="arcon-api-server"
SET GCP_PROJECT="My First Project"
SET GCP_ZONE="asia-south1-c"
SET GOOGLE_APPLICATION_CREDENTIALS=/secrets/g6_bucket_reader.json

REM Build the image based on the Dockerfile
docker build -t %IMAGE_NAME% -f Dockerfile .

REM Run the container
cd ..
docker run  --rm --name %IMAGE_NAME% -ti ^
            --mount type=bind,source="%cd%\api-service",target=/app ^
            --mount type=bind,source="%cd%\persistent-folder",target=/persistent ^
            --mount type=bind,source="%cd%\secrets",target=/secrets ^
            -p 9000:9000 ^
            -e GOOGLE_APPLICATION_CREDENTIALS=%GOOGLE_APPLICATION_CREDENTIALS% ^
            -e GCP_PROJECT=%GCP_PROJECT% ^
            -e GCP_ZONE=%GCP_ZONE% ^
            -e DEV=1 %IMAGE_NAME% 