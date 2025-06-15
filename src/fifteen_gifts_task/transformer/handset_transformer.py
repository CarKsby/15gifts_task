from fifteen_gifts_task.transformer.base import Transformer
from fifteen_gifts_task.models.data_models import Handset
from typing import List

from fifteen_gifts_task.models.table_models import (
    HandsetsTable
)


class HandsetTransformer(Transformer):
    """
    Transformer class for transforming handset data into PyDantic models
    """

    def __init__(self, raw_data: dict):
        super().__init__(raw_data)

    def transform(self: dict) -> None:
        """
        Transform the raw data into PyDantic models
        :param data_obj: The extracted data object
        :return: None
        """
        data = self.get_raw_data()
        if self.is_valid_for_recommendation(data):
            handset_model = Handset(
                **data
            )

            self.transformed_models_list = [handset_model]

    def is_valid_for_recommendation(self, data) -> bool:
        """
        Check if the data is valid for recommendation
        :return: True if valid, False otherwise
        """
        required_fields = [
            "brand",
            "code",
            "name",
            "averageRating",
            "totalReviews",
            "inStock",
            "isFiveGReady",
            "isSwitchUpEligible",
        ]
        return all(field in data for field in required_fields) and (
            data["isDataOnly"] == False and data["isDiscontinuedDevice"] == False
        )

    def set_table_models(self):
        """
        Convert Handset model to Handsets table model
        :param handset_model: The Handset model to convert
        :return: Handsets table model
        """
        handset_table_model = self.transformed_models_list[0]

        handset_table = HandsetsTable(
            brand=handset_table_model.brand,
            code=handset_table_model.code,
            name=handset_table_model.name,
            averageRating=handset_table_model.averageRating,
            totalReviews=handset_table_model.totalReviews,
            inStock=handset_table_model.inStock,
            isFiveGReady=handset_table_model.isFiveGReady,
            isSwitchUpEligible=handset_table_model.isSwitchUpEligible,
            skuCode=handset_table_model.skuCode,
        )
        self.table_models = [handset_table]

    def get_table_models(self) -> List[HandsetsTable]:          
        """
        Get the table models for Handsets
        :return: List of HandsetsTable models
        """
        return self.table_models
