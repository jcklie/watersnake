from typing import Tuple

import numpy as np
from scipy.fftpack import dct, idct
from PIL import Image


class SpreadSpectrumWatermarking:
    """
    Cox, I. J., Kilian, J., Leighton, F. T., & Shamoon, T. (1997).
    Secure spread spectrum watermarking for multimedia. IEEE Transactions on Image
    Processing, 6(12), 1673–1687. doi:10.1109/83.650120
    """

    def __init__(self, n: int, alpha: float = 0.1):
        self.n = n
        self.alpha = alpha

    def mark_array(self, pixels: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        # 1. Extract a sequence of values V = v1 ... vn from the image. We use the n highest
        #    components of the luminance DCT
        # 2. Generate a watermark vector W of length n from a Gaussian with mean 0 and std 1
        # 3. Replace V with V + alpha * W
        img = Image.fromarray(pixels, "RGB")
        height, width = img.size

        # We use YCbCr as we want to smear the watermark in the parts
        # of the image which human perception is very sensitive to,
        # in this case we choose the luminance. Also, the algorithm
        # works on a 2d single-channel image, therefore we need to choose
        # a channel we apply the DCT to when working with color images.
        ycbcr = np.asarray(img.convert("YCbCr"))
        luminance = ycbcr[:, :, 0]

        # We apply the DCT to the luminance channel and find the n largest
        # components. These we alter with our watermark
        dct = _dct2(luminance)

        # Extract n largest components in sorted order
        flattened_dct = dct.flatten(order="C")
        ind = self._get_topk(flattened_dct)

        # The watermark are n values from a Gaussian distribution with
        # mean 0 and standard deviation 1
        mu, sigma = 0, 1
        watermark = np.random.normal(mu, sigma, self.n)

        # Apply the watermark
        flattened_dct_marked = flattened_dct.copy()
        flattened_dct_marked[ind] = flattened_dct[ind] + self.alpha * watermark

        # Convert it back
        dct_marked = flattened_dct_marked.reshape((width, height))
        luminance_marked = _idct2(dct_marked)
        ycbcr_marked = ycbcr.copy()
        ycbcr_marked[:, :, 0] = luminance_marked

        if np.allclose(ycbcr, ycbcr_marked):
            raise RuntimeError("Result image identical to original one. Change either alpha value or watermark size.")

        img_rgb_marked = Image.fromarray(ycbcr_marked, "YCbCr").convert("RGB")
        pixels_rgb_marked = np.asarray(img_rgb_marked)

        return pixels_rgb_marked, watermark

    def mark_image(self, path: str) -> Tuple[np.ndarray, np.ndarray]:
        pixels = np.asarray(Image.open(path))
        return self.mark_array(pixels)

    def extract_from_array(self, data_original: np.ndarray, data_suspect: np.ndarray) -> np.ndarray:
        """ Extract watermark from a 2D array according to spread spectrum watermarking algorithm"""
        luminance_original = np.asarray(Image.fromarray(data_original, "RGB").convert("L"))
        luminance_suspect = np.asarray(Image.fromarray(data_suspect, "RGB").convert("L"))

        dct_original = _dct2(luminance_original)
        dct_suspect = _dct2(luminance_suspect)

        flattened_dct_original = dct_original.flatten(order="C")
        flattened_dct_suspect = dct_suspect.flatten(order="C")
        ind = self._get_topk(flattened_dct_original)

        watermark_suspect = (flattened_dct_suspect[ind] - flattened_dct_original[ind]) / self.alpha

        return watermark_suspect

    def extract_from_image(self, path_original: str, path_suspect: str) -> np.ndarray:
        """ Extract watermark from an image according to spread spectrum watermarking algorithm"""
        img_original = np.asarray(Image.open(path_original))
        img_suspect = np.asarray(Image.open(path_suspect))

        return self.extract_from_array(img_original, img_suspect)

    def similarity(self, original_watermark: np.ndarray, suspicous_watermark: np.ndarray) -> float:
        """ Computes the similarities between original watermark sequence and watermark extracted from
        suspicious image.
        """
        x = original_watermark.dot(suspicous_watermark)
        y = np.sqrt(suspicous_watermark.dot(suspicous_watermark))
        return x / y

    def _get_topk(self, data: np.array) -> np.array:
        """ Returns indices to the top n entries in `data` """
        ind = np.argpartition(data, -self.n)[-self.n :]
        ind = ind[np.argsort(data[ind])][::-1]
        return ind


# implement 2D DCT
def _dct2(a):
    return dct(dct(a.T, norm="ortho").T, norm="ortho")


# implement 2D IDCT
def _idct2(a):
    return idct(idct(a.T, norm="ortho").T, norm="ortho")
