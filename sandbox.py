from watersnake import SpreadSpectrumWatermarking

from skimage.data import chelsea
import imageio

import numpy as np


def test_mark_array():
    s = SpreadSpectrumWatermarking(300, 0.2)

    img_original = chelsea()

    img_marked1, watermark1 = s.mark_array(img_original)
    img_marked2, watermark2 = s.mark_array(img_original)

    suspicious_watermark1 = s.extract_from_array(data_original=img_original, data_suspect=img_marked1)
    suspicious_watermark2 = s.extract_from_array(data_original=img_original, data_suspect=img_marked2)

    compute_similarity(s, watermark1, watermark2, suspicious_watermark1, suspicious_watermark2)


def test_mark_image():
    s = SpreadSpectrumWatermarking(300, 0.1)

    path_original = r"tests/images/lenna.png"
    path_suspect1 = r"lenna_marked1.png"
    path_suspect2 = r"lenna_marked2.png"

    img_marked1, watermark1 = s.mark_image(path_original)
    imageio.imwrite(path_suspect1, img_marked1.astype(np.uint8))

    img_marked2, watermark2 = s.mark_image(path_original)
    imageio.imwrite(path_suspect2, img_marked2.astype(np.uint8))

    suspicious_watermark1 = s.extract_from_image(path_original=path_original, path_suspect=path_suspect1)
    suspicious_watermark2 = s.extract_from_image(path_original=path_original, path_suspect=path_suspect2)

    compute_similarity(s, watermark1, watermark2, suspicious_watermark1, suspicious_watermark2)


def compute_similarity(s, watermark1, watermark2, suspicious_watermark1, suspicious_watermark2):
    similarity11 = s.similarity(watermark1, suspicious_watermark1)
    similarity22 = s.similarity(watermark2, suspicious_watermark2)
    similarity12 = s.similarity(watermark1, suspicious_watermark2)
    similarity21 = s.similarity(watermark2, suspicious_watermark1)

    print(similarity11, "should be high")
    print(similarity22, "should be high")
    print(similarity12, "should be low")
    print(similarity21, "should be low")


def main():
    print("Image")
    test_mark_image()
    print("Array")
    test_mark_array()




if __name__ == "__main__":
    main()