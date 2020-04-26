import os
import unittest

import imageio
import numpy as np
from skimage.data import astronaut, data_dir

from watersnake import SpreadSpectrumWatermarking


class TestSpreadSpectrumWatermarking(unittest.TestCase):
    def test_mark_array(self):
        s = SpreadSpectrumWatermarking(500, 0.5)

        img_original = astronaut()

        img_marked1, watermark1 = s.mark_array(img_original)
        img_marked2, watermark2 = s.mark_array(img_original)

        suspicious_watermark1 = s.extract_from_array(data_original=img_original, data_suspect=img_marked1)
        suspicious_watermark2 = s.extract_from_array(data_original=img_original, data_suspect=img_marked2)

        similarity11 = s.similarity(watermark1, suspicious_watermark1)
        similarity12 = s.similarity(watermark1, suspicious_watermark2)

        similarity22 = s.similarity(watermark2, suspicious_watermark2)
        similarity21 = s.similarity(watermark2, suspicious_watermark1)

        # We check that using the real watermark 1 yields higher similarity
        self.assertGreater(similarity11, similarity12)
        self.assertGreater(similarity11 - similarity12, 2)

        # We check that using the real watermark 2 yields higher similarity
        self.assertGreater(similarity22, similarity21)
        self.assertGreater(similarity22 - similarity21, 2)

    def test_mark_image(self):
        s = SpreadSpectrumWatermarking(500, 0.5)

        path_original = os.path.join(data_dir, "astronaut.png")
        path_suspect1 = r"marked1.png"
        path_suspect2 = r"marked2.png"

        img_marked1, watermark1 = s.mark_image(path_original)
        imageio.imwrite(path_suspect1, img_marked1.astype(np.uint8))

        img_marked2, watermark2 = s.mark_image(path_original)
        imageio.imwrite(path_suspect2, img_marked2.astype(np.uint8))

        suspicious_watermark1 = s.extract_from_image(path_original=path_original, path_suspect=path_suspect1)
        suspicious_watermark2 = s.extract_from_image(path_original=path_original, path_suspect=path_suspect2)

        similarity11 = s.similarity(watermark1, suspicious_watermark1)
        similarity12 = s.similarity(watermark1, suspicious_watermark2)

        similarity22 = s.similarity(watermark2, suspicious_watermark2)
        similarity21 = s.similarity(watermark2, suspicious_watermark1)

        # We check that using the real watermark 1 yields higher similarity
        self.assertGreater(similarity11, similarity12)
        self.assertGreater(similarity11 - similarity12, 2)

        # We check that using the real watermark 2 yields higher similarity
        self.assertGreater(similarity22, similarity21)
        self.assertGreater(similarity22 - similarity21, 2)

    def setUp(self) -> None:
        np.random.seed(42)


if __name__ == "__main__":
    unittest.main()
