from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse
from pathlib import Path
import shutil

from src.jobs.store import create_job, update_job, get_job
from src.utils.cleanup import cleanup_old_outputs
from src.agents.video_agent import run_full_pipeline, run_dubb_pipeline


app = FastAPI()

BASE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_DIR = BASE_DIR / "assets" / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

@app.on_event("startup")
def startup_cleanup():
    cleanup_old_outputs(OUTPUT_DIR)

@app.get("/")
def root():
    return {"status": "api running"}


@app.post("/process-video")
async def process_video(
    background_tasks: BackgroundTasks,
    file: UploadFile
):
    job_id = create_job()
    input_path = OUTPUT_DIR / f"{job_id}_{file.filename}"

    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    background_tasks.add_task(
        process_pipeline,
        job_id,
        input_path
    )

    return {"job_id": job_id}


def process_pipeline(job_id: str, video_path: Path):
    try:
        update_job(job_id, "PROCESSING")

        run_full_pipeline(
            video_path=str(video_path),
            output_path=str(OUTPUT_DIR)
        )

        final_output = OUTPUT_DIR / "output_with_blur.mp4"
        update_job(job_id, "COMPLETED", str(final_output))

    except Exception as e:
        update_job(job_id, "FAILED", str(e))


@app.post("/dubb-video")
async def dubb_video(background_tasks: BackgroundTasks, file: UploadFile):
    job_id = create_job()
    input_path = OUTPUT_DIR / f"{job_id}_{file.filename}"

    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    background_tasks.add_task(
        process_dubb_pipeline,
        job_id,
        input_path
    )

    return {"job_id": job_id}


def process_dubb_pipeline(job_id: str, video_path: Path):
    try:
        update_job(job_id, "PROCESSING")

        run_dubb_pipeline(
            video_path=str(video_path),
            output_path=str(OUTPUT_DIR)
        )

        final_output = OUTPUT_DIR / "dubb_output.mp4"
        update_job(job_id, "COMPLETED", str(final_output))

    except Exception as e:
        update_job(job_id, "FAILED", str(e))

@app.get("/status/{job_id}")
def status(job_id: str):
    job = get_job(job_id)
    if not job:
        return {"error": "Job not found"}
    return job


@app.get("/download/{job_id}")
def download(job_id: str):
    job = get_job(job_id)
    if not job or job["status"] != "COMPLETED":
        return {"error": "Not ready"}

    return FileResponse(
        job["output"],
        media_type="video/mp4",
        filename="processed_video.mp4"
    )
