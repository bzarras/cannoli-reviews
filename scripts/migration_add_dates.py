import sys
import os
import datetime

# Get the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Get the project's root directory (one level up from the script directory)
project_root = os.path.abspath(os.path.join(script_dir, '..'))

# Add the project's root directory to the Python path
sys.path.append(project_root)


from sqlalchemy import select
from app import tables
from app.db import SessionLocal


def update_time(item, db):
    now = datetime.datetime.utcnow()
    should_update = False
    if item.created_at is None:
        item.created_at = now
        should_update = True
    if item.updated_at is None:
        item.updated_at = now
        should_update = True
    if should_update:
        db.add(item)


def main():
    print("Running dates migration")

    # create session
    db = SessionLocal()

    # get all images
    images = db.scalars(
        statement=select(tables.Image)
    )

    # get all reviews
    reviews = db.scalars(
        statement=select(tables.Review)
    )

    for image in images:
        update_time(image, db)
    
    for review in reviews:
        update_time(review, db)

    # save to database
    db.commit()
    db.close()


if __name__ == "__main__":
    main()
