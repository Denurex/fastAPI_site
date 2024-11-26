
from pathlib import Path

from PIL import Image

from app.tasks.celeryy import celery_app


@celery_app.task
def process_pic(path: str):
    img_path = Path(path)
    image = Image.open(img_path)
    image_resized_1000_500 = image.resize((1000, 500))
    image_resized_1000_500.save(f'static/images/resized_1000_500_{img_path.name}')