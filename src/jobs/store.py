import uuid

JOBS = {}

def create_job():
    job_id = str(uuid.uuid4())
    JOBS[job_id] = {"status": "PENDING", "output": None}
    return job_id

def update_job(job_id, status, output=None):
    JOBS[job_id]["status"] = status
    if output:
        JOBS[job_id]["output"] = output

def get_job(job_id):
    return JOBS.get(job_id)
