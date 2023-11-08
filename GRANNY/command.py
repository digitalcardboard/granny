import os

from . import GRANNY_StarchArea

import argparse

from GRANNY import (
    GRANNY_BlushColor,
    GRANNY_PeelColor,
    GRANNY_Segmentation,
    GRANNY_SuperficialScald,
)

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"


def main():
    parser = argparse.ArgumentParser(
        description="Implementation of Mask-RCNN and image binarization to rate disorder severity on Granny Smith apples."
    )

    parser.add_argument(
        "-a",
        "--action",
        dest="action",
        type=str,
        nargs="?",
        required=True,
        help="Required. Specify an action to perform.",
    )

    parser.add_argument(
        "-d",
        "--image_dir",
        dest="dir",
        type=str,
        nargs="?",
        required=True,
        help="Required. Specify a directory or a file.",
    )

    parser.add_argument(
        "-n",
        "--num_instances",
        dest="num_instances",
        type=int,
        nargs="?",
        required=False,
        help="Optional, default is 18. The number of instances on each image.",
    )

    args = parser.parse_args()

    if args.action == "extract":
        GRANNY_Segmentation.GrannySegmentation(
            args.action, args.dir, args.num_instances
        ).extract_instances_with_MaskRCNN()
    elif args.action == "scald":
        GRANNY_SuperficialScald.GrannySuperficialScald(
            args.action, args.dir
        ).GrannySuperficialScald()
    elif args.action == "peel":
        GRANNY_PeelColor.GrannyPeelColor(
            args.action, args.dir
        ).GrannyPeelColor()
    elif args.action == "starch":
        GRANNY_StarchArea.GrannyStarchArea(
            args.action, args.dir
        ).GrannyStarchArea()
    elif args.action == "blush":
        GRANNY_BlushColor.GrannyPearBlush(
            args.action, args.dir
        ).GrannyPearBlush()
    else:
        print("\t- Invalid Action. -")
