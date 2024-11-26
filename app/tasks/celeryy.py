from celery import Celery

from app.config import settings

celery_app = Celery(
    'tasks',
    include=['app.tasks.tasks'],
    broker=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}'
)

# celery_app.autodiscover_tasks(['app.tasks'], force=True)