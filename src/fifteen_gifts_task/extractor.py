from abc import ABC, abstractmethod
import json
import logging

logger = logging.getLogger(__name__)


class Extractor(ABC):
    """
    Base class for various extraction methods from different data sources to Python objects
    """

    def __init__(self):
        self.data_obj = None

    @abstractmethod
    def extract(self, file_URI: str) -> None:
        """
        method to extract
        :param data: Location of data file
        :return: None
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def set_data_obj(self, data_obj) -> None:
        """
        Set the data object after extraction
        :param data_obj: The extracted data object
        :return: None
        """
        self.data_obj = data_obj

    def get_data_obj(self):
        """
        Get the extracted data object
        :return: The extracted data object
        """
        return self.data_obj


class JSONFileExtractor(Extractor):
    """
    Extractor for JSON data
    """

    def extract(self, file_URI: str) -> None:
        try:
            with open(file_URI, "r") as file:
                self.set_data_obj(json.load(file))
            logger.info(f"Successfully extracted data from {file_URI}")
        except Exception as e:
            logger.error(f"Failed to extract data from {file_URI}: {e}")
            raise e
        return self.get_data_obj()
