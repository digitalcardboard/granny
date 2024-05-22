import os
from datetime import datetime
from multiprocessing import Pool
from typing import List, Tuple, cast

import cv2
import numpy as np
from Granny.Analyses.Analysis import Analysis
from Granny.Analyses.Parameter import IntParam, StringParam
from Granny.Models.Images.Image import Image
from Granny.Models.IO.RGBImageFile import RGBImageFile
from numpy.typing import NDArray


class StarchArea(Analysis):

    __analysis_name__ = "starch"

    def __init__(self, images: List[Image]):
        Analysis.__init__(self, images)

        # default threshold parameter
        threshold = IntParam(
            "th",
            "threshold",
            "The color threhsold that distinguishes iodine-stained starch regions",
        )
        threshold.setMin(0)
        threshold.setMax(255)
        threshold.setDefaultValue(172)
        self.addParam(threshold)

    def drawMask(self, img: NDArray[np.uint8], mask: NDArray[np.uint8]) -> NDArray[np.uint8]:
        """
        Overlays a binary mask on an image.

        Args:
            - img: The input image where the mask will be applied.
            - mask: The binary mask to be overlied on the image.
        """
        result = img.copy()
        color = (0, 0, 0)
        alpha = 0.6
        for c in range(3):
            result[:, :, c] = np.where(
                mask == 0,
                result[:, :, c] * (1 - alpha) + alpha * color[c],
                result[:, :, c],
            )
        return result

    def calculateStarch(self, img: NDArray[np.uint8]) -> Tuple[float, NDArray[np.uint8]]:
        """ """

        def extractImage(img: NDArray[np.uint8]):
            """
            Extracts minimum and maximum pixel value of an image
            """
            hist, _ = np.histogram(gray, bins=256, range=(0, 255))
            low = (hist != 0).argmax()
            high = 255 - (hist[::-1] != 0).argmax()
            return low, high

        def adjustImage(
            img: NDArray[np.uint8], lIn: int, hIn: int, lOut: int = 0, hOut: int = 255
        ):
            """
            Adjusts the intensity values of an image I to new values. This function is equivalent
            to normalize the image pixel values to [0, 255].
            """
            # Ensure img is in the range [lIn, hIn]
            img = np.clip(img, lIn, hIn)

            # Normalize the image to the range [0, 1]
            out = (img - lIn) / (hIn - lIn)

            # Scale and shift the normalized image to the range [lOut, hOut]
            out = out * (hOut - lOut) + lOut

            return out.astype(np.uint8)

        new_img = img.copy()
        img = cast(NDArray[np.uint8], cv2.GaussianBlur(img, (11, 11), 0))
        gray = cast(NDArray[np.uint8], cv2.cvtColor(img, cv2.COLOR_RGB2GRAY))

        # re-adjusts the image to [0 255]
        low, high = extractImage(gray)
        gray = adjustImage(gray, low, high)

        # create thresholded matrices
        threshold = np.logical_and((gray > 0), (gray <= 172)).astype(np.uint8)

        # creates new image using threshold matrices
        new_img = self.drawMask(new_img, threshold)

        ground_truth = np.count_nonzero(
            cast(NDArray[np.uint8], cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)) > 0
        )
        starch = np.count_nonzero(threshold)

        return starch / ground_truth, new_img

    def rateImageInstance(self, image_instance: Image) -> Image:
        """
        1. Loads and performs analysis on the provided Image instance.
        2. Saves the instance to result directory

        @param image_instance: An GRANNY.Models.Images.Image instance

        @return
            image_name: file name of the image instance
            score: rating for the instance
        """
        # initiates ImageIO
        image_io = RGBImageFile(image_instance.getFilePath())

        # loads image from file system with RGBImageFile(ImageIO)
        image_instance.loadImage(image_io=image_io)

        # gets array image
        img = image_instance.getImage()

        # performs starch percentage calculation
        score, new_img = self.calculateStarch(img)

        # calls IO to save the image
        image_io.saveImage(new_img, self.__analysis_name__)

        return image_instance

    def performAnalysis(self):
        """
        {@inheritdoc}
        """
        # generate metadata of the analysis
        self.generateAnalysisMetadata()

        # perform analysis with multiprocessing
        num_cpu = os.cpu_count()
        cpu_count = int(num_cpu * 0.8) or 1  # type: ignore
        with Pool(cpu_count) as pool:
            pool.map(self.rateImageInstance, self.images)
