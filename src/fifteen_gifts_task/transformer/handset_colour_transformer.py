from fifteen_gifts_task.transformer.base import Transformer
from fifteen_gifts_task.models.data_models import HandsetColour
from fifteen_gifts_task.models.table_models import HandsetColourTable
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class HandsetColourTransformer(Transformer):
    """
    Transformer class for transforming colour data into PyDantic models
    """

    def __init__(self, raw_data: Dict[str, any]) -> None:
        super().__init__(raw_data)

    def transform(self) -> None:
        """
        Transform the raw data into PyDantic models
        :return: None
        """
        data = self.get_raw_data()
        colour_handsets_list = data["deviceOptions"]
        for colour_handsets in colour_handsets_list:
            if self.is_valid_for_recommendation(colour_handsets["color"]):
                colour_model = HandsetColour(**colour_handsets["color"])
                self.transformed_models_list.append(colour_model)

        return

    def is_valid_for_recommendation(self, colour_data: dict) -> bool:
        """
        Check if the data is valid for recommendation
        :return: True if valid, False otherwise
        """
        required_fields = ["name", "hexCode"]
        return (
            all(field in colour_data for field in required_fields)
            and colour_data["isAvailable"] == True
        )

    def set_table_models(self) -> None:
        """
        Convert HandsetColour model to HandsetColour table model
        :return: None
        """
        self.table_models = [
            HandsetColourTable(**colour_model.model_dump())
            for colour_model in self.transformed_models_list
        ]
        return

    def get_table_models(self) -> List[HandsetColourTable]:
        """
        Get the table models for HandsetColour
        :return: List of HandsetColourTable models
        """
        return self.table_models
