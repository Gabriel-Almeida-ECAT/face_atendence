import os
import face_recognition
import numpy as np
import datetime

from PIL import Image
from wand.image import Image as wand_image
from wand.exceptions import WandException

def recognize(img: np.uint8, db_path: str) -> str:
    face_scan_result: list[bytes] = face_recognition.face_encodings(img)
    if len(face_scan_result) == 0:
        return 'no_person_found'
    else:
        face_scan_result: bytes = face_scan_result[0]

    db_imgs_list: list[str] = sorted(os.listdir(db_path))

    match: bool = False
    ind: int = 0
    while (not match) and (ind < len(db_imgs_list)):
        img_path: str = os.path.join(db_path, db_imgs_list[ind])

        with open(img_path, 'rb') as img_file:
            test_img = Image.open(img_file)
            test_img = np.array(test_img)

        test_img_encoding = face_recognition.face_encodings(test_img)
        if test_img_encoding:
            match = face_recognition.compare_faces([test_img_encoding[0]], face_scan_result)
        ind += 1

    if match:
        return db_imgs_list[ind-1]
    else:
        return 'person_not_registered'


def fixCorruptJpeg(input_path, output_path):
    try:
        with wand_image(filename=input_path) as img:
            img.format = 'jpeg'
            img.save(filename=output_path)

            return True

    except WandException as e:
        return False


def main() -> None:
    pass


if __name__ == '__main__':
    main()