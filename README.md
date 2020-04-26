# watersnake

Currently contains a a simple spread-spectrum based informed watermarking implementation in Python.
It is based on the paper [Ingemar J. Cox, Joe Kilian, F. Thomson Leighton, and Talal Shamoon, "Secure Spread 
Spectrum Watermarking for Multimedia," IEEE Trans. on Image Processing, Dec. 1997](http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=650120).

## Usage
   
````python
from watersnake import SpreadSpectrumWatermarking

s = SpreadSpectrumWatermarking(300, 0.2)

path_original = r"original.png"
path_suspect1 = r"marked1.png"
path_suspect2 = r"marked2.png"

# Mark images with two different watermarks and save the resulting images
img_marked, watermark1 = s.mark_image(path_original)
img_marked.save(path_suspect1, "png")

img_marked, watermark2 = s.mark_image(path_original)
img_marked.save(path_suspect2, "png")

# Extract watermarks from previously marked images
suspicious_watermark1 = s.extract_from_image(path_original=path_original, path_suspect=path_suspect1)
suspicious_watermark2 = s.extract_from_image(path_original=path_original, path_suspect=path_suspect2)

# Compute pairwise similarity between all 4 combinations. The similarity between
# a watermark and its extracted counterpart should be high, the similarity between
# two different watermarks should be low 
similarity11 = s.similarity(watermark1, suspicious_watermark1)
similarity22 = s.similarity(watermark2, suspicious_watermark2)
similarity12 = s.similarity(watermark1, suspicious_watermark2)
similarity21 = s.similarity(watermark2, suspicious_watermark1)

print(similarity11, "should be high")
print(similarity22, "should be high")
print(similarity12, "should be low")
print(similarity21, "should be low")
````

## Acknowledgements

Loosley based on [israkir/cox-watermarking](https://github.com/israkir/cox-watermarking/blob/master/README.md) .

