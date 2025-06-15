from pydantic import BaseModel
from typing import List, Dict

from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class Transformer(ABC):
    """
    Base class for various transformation of data from Extractor classes to PyDantic models
    """

    def __init__(self, raw_data: Dict[str, any]):
        self.raw_data = raw_data
        self.transformed_models_list: List[BaseModel] = []
        self.invalid_data: List[Dict[str, any]] = []
        self.table_models: List = []

    @abstractmethod
    def transform(self, data_obj) -> None:
        """
        Entrypoint for transforming the data object into PyDantic models
        :param data_obj: The extracted data object
        :return: None
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def is_valid_for_recommendation(self, data=None) -> bool:
        """
        Check if the data is valid for recommendation
        :return: True if valid, False otherwise
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def get_raw_data(self):
        """
        Get the transformed data object
        :return: The transformed data object
        """
        return self.raw_data

    def get_transformed_models_list(self) -> Dict[str, List[BaseModel]]:
        """
        Get the transformed models map
        :return: A dictionary of transformed models
        """
        return self.transformed_models_list
