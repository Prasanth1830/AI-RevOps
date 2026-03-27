"""
Celery Worker Configuration
Background job processing for agent tasks
"""
from celery import Celery
import asyncio
import os

# Celery configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "revops_worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 min timeout
    worker_prefetch_multiplier=1,
    worker_concurrency=4
)


@celery_app.task(bind=True, name="run_agent_task")
def run_agent_task(self, agent_type: str, input_data: dict):
    """Run an agent task asynchronously via Celery"""
    from services.orchestrator import execute_agent

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        result = loop.run_until_complete(
            execute_agent(agent_type, input_data)
        )
        return result
    finally:
        loop.close()


@celery_app.task(name="health_check")
def health_check():
    """Simple health check task"""
    return {"status": "ok", "worker": "active"}
