from abc import ABC, abstractmethod
from typing import Any

import torch
from torch.backends import mps


class AIModel(ABC):
    def __init__(self, model_dir: str):
        self.model_dir: str = model_dir
        self.model: Any
        self.device = (
            "cuda:0" if torch.cuda.is_available(
            ) else "mps" if mps.is_available() else "cpu"
        )

    @abstractmethod
    def loadModel(self):
        """
        Instantiates Yolo model for segmentation
        """
        pass