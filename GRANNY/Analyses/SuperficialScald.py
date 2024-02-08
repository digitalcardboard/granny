from typing import Any, Tuple, cast

import cv2
import numpy as np
from GRANNY.Analyses.Analysis import Analysis
from GRANNY.Models.Images.Image import Image
from numpy.typing import NDArray


class SuperficialScald(Analysis):

    __anlaysis_name__ = "scald"

    def __init__(self, image: Image):
        Analysis.__init__(self, image)

    def getParams(self):
        pass

    def setResults(self, index: int, key: str, value: Any):
        pass

    def checkParams(self):
        pass

    def setParamValue(self, key: str, value: str) -> None:
        pass

    def getParamValue(self, key: str):
        pass

    def getParamKeys(self) -> None:
        pass

    def smoothMask(self, bin_mask: NDArray[np.uint8]) -> NDArray[np.uint8]:
        """
        Smooth scald region with basic morphological operations.
        By performing morphology, the binary mask will be smoothened to avoid discontinuity.
        """
        bin_mask = bin_mask

        # create a circular structuring element of size 10
        ksize = (10, 10)
        strel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ksize=ksize)

        # using to structuring element to perform one close and one open operation on the binary mask
        bin_mask = cv2.dilate(
            cv2.erode(bin_mask, kernel=strel, iterations=1),
            kernel=strel,
            iterations=1,
        )
        bin_mask = cv2.erode(
            cv2.dilate(bin_mask, kernel=strel, iterations=1),
            kernel=strel,
            iterations=1,
        )
        return bin_mask

    def isolateScald(self, img: NDArray[np.uint8]) -> Tuple[NDArray[np.uint8], NDArray[np.uint8]]:
        """
        Remove the scald region from the individual apple images.
        Note that the stem could have potentially been removed during the process.
        """
        # convert from RGB to Lab color space
        new_img = img.copy()
        lab_img = cast(NDArray[np.uint8], cv2.cvtColor(img, cv2.COLOR_RGB2LAB))

        def calculate_threshold_from_hist(hist: NDArray[np.int8]) -> int:
            hist_range = 255 - (hist[::-1] != 0).argmax() - (hist != 0).argmax()
            threshold = np.max(np.argsort(hist)[-10:])
            threshold = int(threshold - 1 / 3 * hist_range)
            threshold = 100 if threshold < 100 else int(threshold)
            return threshold

        # create binary matrices
        hist, _ = np.histogram(lab_img[:, :, 1], bins=256, range=(0, 255))
        threshold_value = calculate_threshold_from_hist(hist)
        threshold_1 = np.logical_and((lab_img[:, :, 0] >= 1), (lab_img[:, :, 0] <= 255))
        threshold_2 = np.logical_and(
            (lab_img[:, :, 1] >= 1), (lab_img[:, :, 1] <= threshold_value)
        )
        threshold_3 = np.logical_and((lab_img[:, :, 2] >= 1), (lab_img[:, :, 2] <= 255))

        # combine to one matrix
        th123 = np.logical_and(np.logical_and(threshold_1, threshold_2), threshold_3).astype(
            np.uint8
        )

        # perform simple morphological operation to smooth the binary mask
        th123 = self.smoothMask(th123)

        # apply the binary mask on the image
        for i in range(3):
            new_img[:, :, i] = new_img[:, :, i] * th123
        return th123, new_img

    def removeTrayResidue(self, img: NDArray[np.uint8]) -> NDArray[np.uint8]:
        """
        Remove the surrounding purple from the individual apples using YCrCb color space.
        This function helps remove the unwanted regions for more precise calculation of the scald area.
        """
        # convert RGB to YCrCb
        new_img = img.copy()
        ycc_img = cast(NDArray[np.uint8], cv2.cvtColor(img, cv2.COLOR_RGB2YCrCb))

        # create binary matrices
        threshold_1 = np.logical_and((ycc_img[:, :, 0] >= 0), (ycc_img[:, :, 0] <= 255))
        threshold_2 = np.logical_and((ycc_img[:, :, 1] >= 0), (ycc_img[:, :, 1] <= 255))
        threshold_3 = np.logical_and((ycc_img[:, :, 2] >= 0), (ycc_img[:, :, 2] <= 126))

        # combine to one matrix
        th123 = np.logical_and(np.logical_and(threshold_1, threshold_2), threshold_3).astype(
            np.uint8
        )

        # create new image using threshold matrices
        for i in range(3):
            new_img[:, :, i] = new_img[:, :, i] * th123
        return new_img

    def score_image(
        self, img: NDArray[np.uint8]
    ) -> Tuple[NDArray[np.uint8], NDArray[np.uint8], NDArray[np.uint8]]:
        """
        Clean up individual image (remove purple area of the tray), and remove scald
        """

        # removes the residue tray background
        img = self.removeTrayResidue(img)
        nopurple_img = img.copy()

        # Image smoothing
        img = cv2.GaussianBlur(img, (3, 3), sigmaX=0, sigmaY=0)

        # Removal of scald regions
        bw, img = self.isolateScald(img)

        return nopurple_img, img, bw

    def calculateScald(self, bw: NDArray[np.uint8], img: NDArray[np.uint8]) -> float:
        """
        Calculate scald region by counting all non zeros area

        Args:
                (numpy.array) bw: binarized image
                (numpy.array) img: original image to be used as ground truth

        Returns:
                (float) fraction: the scald region, i.e. fraction of the original image that was removed
        """
        # count non zeros of binarized image
        ground_area = 1 / 3 * np.count_nonzero(img[:, :, 0:2])

        # count non zeros of original image
        mask_area = 1 / 3 * np.count_nonzero(bw[:, :, 0:2])

        # calculate fraction
        fraction = 0
        if ground_area == 0:
            return 1
        else:
            fraction = 1 - mask_area / ground_area
        if fraction < 0:
            return 0
        return fraction

    def rateSuperficialScald(self, img: NDArray[np.uint8]) -> float:
        # returns apple image with no scald
        nopurple_img, binarized_image, bw = self.score_image(img)

        # calculate the scald region and save image
        score = self.calculateScald(binarized_image, nopurple_img)
        return score

    def performAnalysis(self) -> None:
        # loads image from file system with RGBImageFile(ImageIO)
        self.image.loadImage()
        # gets array image
        img = self.image.getImage()
        # performs starch percentage calculation
        result = self.rateSuperficialScald(img)
        print(result)