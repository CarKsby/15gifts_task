from fifteen_gifts_task.transformer.base import Transformer
from fifteen_gifts_task.models.data_models import Extras
from fifteen_gifts_task.models.table_models import ExtraOffersTable
from typing import Dict, List


class ExtrasTransformer(Transformer):
    """
    Transformer class for transforming extras data into PyDantic models
    """

    def __init__(self, raw_data: Dict[str, any]):
        super().__init__(raw_data)

    def transform(self) -> None:
        """
        Transform the raw data into PyDantic models
        :return: None
        """
        data = self.get_raw_data()
        tariff_data_list = data["tariffCardDetails"]["tariffCards"]
        for tariff_data in tariff_data_list:
            extras_list = tariff_data["extras"]
            for extras in extras_list:
                extras_model = Extras(**extras)
                self.transformed_models_list.append(extras_model)

        self.dedupe_extras()

    def is_valid_for_recommendation(self, data=None) -> bool:
        return True

    def dedupe_extras(self) -> None:
        """
        Deduplicate extras before inserting into the database
        :return: None
        """
        self.transformed_models_list = list(set(self.transformed_models_list))
        return

    def set_table_models(self) -> ExtraOffersTable:
        """
        Convert Extras model to ExtraOffers table model
        :param extras_model: The Extras model to convert
        :return: ExtraOffers table model
        """
        self.table_models = [
            ExtraOffersTable(**extras_model.model_dump())
            for extras_model in self.transformed_models_list
        ]
    

    def get_table_models(self) -> List[ExtraOffersTable]:
        """
        Get the table models for Extras
        :return: List of ExtraOffersTable models
        """
        return self.table_models
