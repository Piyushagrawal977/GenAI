from fastapi import FastAPI, Query
from .client.rq_client import queue
from .queues.worker import processor

app=FastAPI()

@app.get("/")
def root():
    return {"status": "server is up and running!"}

@app.post("/chat")
def chat(
    query:str=Query(...,description="The chat query of the user")
):
    job=queue.enqueue(processor,query)
    return {"status":"queued", "job_id":job.id}

@app.get("/job-status")
def result(
    job_id:str=Query(..., description="Job id")
):
    job = queue.fetch_job(job_id=job_id)
    try:
        result = job.return_value()
        return {"result":result}
    except:
        return {"error":"something went wrong"}