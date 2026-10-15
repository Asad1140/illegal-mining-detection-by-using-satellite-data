from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import numpy as np

class BaseChangeDetectionModel(ABC):
    """Abstract interface for temporal change detection models (Siamese CNN, Temporal Transformer, Spectral)."""
    
    @property
    @abstractmethod
    def model_name(self) -> str:
        pass

    @property
    @abstractmethod
    def model_status(self) -> str:
        """Returns 'Trained Production Model' or 'Prototype / Demo Model'."""
        pass

    @abstractmethod
    def detect_change(self, t1_features: Dict[str, Any], t2_features: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Infers change probability map and metrics between time T1 and T2."""
        pass

class BaseSegmentationModel(ABC):
    """Abstract interface for land-use and mining disturbance segmentation (U-Net, SegFormer)."""

    CLASSES = {
        0: "Background",
        1: "Vegetation",
        2: "Water",
        3: "Bare Land",
        4: "Rock",
        5: "Road",
        6: "Settlement",
        7: "Active Mining Pit",
        8: "Overburden Dump",
        9: "Stockpile",
        10: "Construction",
        11: "Forest Clearance"
    }

    @property
    @abstractmethod
    def model_name(self) -> str:
        pass

    @property
    @abstractmethod
    def model_status(self) -> str:
        pass

    @abstractmethod
    def segment(self, multispectral_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Segments input imagery into 12 land-cover/mining disturbance classes."""
        pass

class BaseRiskModel(ABC):
    """Abstract interface for risk scoring and factor attribution."""

    @abstractmethod
    def calculate_risk(self, factors: Dict[str, Any], custom_weights: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """Calculates 0-100 risk score and explainable factor breakdown."""
        pass

class BasePredictiveExpansionModel(ABC):
    """Abstract interface for predicting historical mining expansion direction and rate."""

    @abstractmethod
    def predict_expansion(self, historical_observations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculates expansion rate (%) and projected next-risk zone polygon."""
        pass
