from fifteen_gifts_task.transformer.base import Transformer
from fifteen_gifts_task.models.data_models import Tariff
from fifteen_gifts_task.models.table_models import TariffPlanTable
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class HandsetTariffTransformer(Transformer):
    """
    Transformer class for transforming handset tariff data into PyDantic models
    """

    def __init__(self, raw_data: Dict[str, any]):
        super().__init__(raw_data)

    def transform(self) -> None:
        """
        Transform the raw data into PyDantic models
        :return: None
        """
        data = self.get_raw_data()
        logging.debug(data["tariffCardDetails"])
        tariff_list = data["tariffCardDetails"]["tariffCards"]
        for tariff in tariff_list:
            if self.is_valid_for_recommendation(tariff):
                tariff_model = Tariff(
                    **tariff,
                    api=self.extract_api(tariff)
                )
                self.transformed_models_list.append(tariff_model)

    def is_valid_for_recommendation(self, data: Dict[str, any]) -> bool:
        """
        Check if the data is valid for recommendation
        :return: True if valid, False otherwise
        """
        return True

    def extract_api(self, api_mapping: Dict[str, any]) -> None:
        """
        Extract and transform the raw data into PyDantic models
        :param data: The raw data to be transformed
        :return: None
        """
        return float(api_mapping["apiPriceDetails"]["price"][1:])
    
    def set_table_models(self) -> None:
        """
        Convert Tariff model to TariffPlan table model
        :return: None
        """

        for tariff_model in self.transformed_models_list:
            self.table_models.append(
                TariffPlanTable(
                    planOfferingCode=tariff_model.planOfferingCode,
                    name=tariff_model.name,
                    totalUpfront=tariff_model.totalUpfront,
                    airtimeMrc=tariff_model.airtimeMrc,
                    deviceMrc=tariff_model.deviceMrc,
                    api=tariff_model.api,
                    contractDuration=tariff_model.contractDuration,
                )
            )
    
    def get_table_models(self) -> List:
        """
        Get the transformed table models
        :return: A list of transformed table models
        """
        return self.table_models