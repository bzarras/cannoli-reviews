import sys
import os
import hashlib

# Get the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Get the project's root directory (one level up from the script directory)
project_root = os.path.abspath(os.path.join(script_dir, '..'))

# Add the project's root directory to the Python path
sys.path.append(project_root)


from sqlalchemy import select
from app import tables
from app.db import SessionLocal


def main():
    print("Running etag migration")

    # create session
    db = SessionLocal()

    # get all images
    images = db.scalars(
        statement=select(tables.Image)
    )

    # create etag for each image and add it to session
    for image in images:
        if image.etag is None:
            image_data = image.data
            etag = hashlib.md5(image_data).hexdigest()
            print(f"setting new etag {etag} on image {image.name}")
            image.etag = etag
            db.add(image)

    # save to database
    db.commit()
    db.close()


if __name__ == "__main__":
    main()
