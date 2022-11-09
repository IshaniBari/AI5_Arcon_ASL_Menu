from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import asyncio
import os
from fastapi import File
from tempfile import TemporaryDirectory
# from api.tracker import TrackerService
from api import tracker
from api import model

# Initialize Tracker Service
# tracker_service = TrackerService()

# Setup FastAPI app
app = FastAPI(
    title="API Server",
    description="API Server",
    version="v1"
)

# Enable CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    # Startup tasks
    # Start the tracker service
    # asyncio.create_task(tracker_service.track())
    gcp_project = os.environ["GCP_PROJECT"]
    bucket_name = "asl_best_model"
    # local_experiments_path = "/persistent/experiments"
    persistent_folder = "/persistent"
    download_file = "Best_Model.h5"
    tracker.download_blob(bucket_name, download_file,os.path.join(persistent_folder, download_file))
    print("Download completed!")

# Routes
@app.get("/")
async def get_index():
    return {
        "message": "Welcome to the API Service"
    }


@app.post("/predict")
async def predict(
        file: bytes = File(...)
):
    print("predict file:", len(file), type(file))

    # Save the image
    with TemporaryDirectory() as image_dir:
        image_path = os.path.join(image_dir, "test.png")
        with open(image_path, "wb") as output:
            output.write(file)

        # Make prediction
        prediction_results = model.make_prediction(image_path)

    return prediction_results
