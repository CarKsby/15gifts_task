from sqlalchemy.orm import sessionmaker
from typing import List
import logging
from sqlalchemy import create_engine
from abc import ABC, abstractmethod
from typing import Dict

from fifteen_gifts_task.models.table_models import Base, ExtraOffersTable, HandsetsTable, TariffPlanTable


logger = logging.getLogger(__name__)


class BaseLoader(ABC):
    """
    Base class for various loading methods to persist data into a database
    """

    def __init__(self):
        self.engine = create_engine("sqlite:///o2_inventory.sqlite3", echo=True)
        Base.metadata.create_all(self.engine)



class Loader(BaseLoader):
    """
    Loader class for persisting data into a database
    """

    def __init__(self):
        super().__init__()
        self.session = sessionmaker(bind=self.engine)


    def load_extras(self, extra_rows:List[ExtraOffersTable], session) -> None:
        try:
            session.add_all(extra_rows)
            session.commit()
            logging.info("Extras loaded successfully.")
            return
        except Exception as e:
            session.rollback()
            logging.error(f"Error loading extra rows: {e}")
            return
        

    def load_handsets(self, handset_table_model: HandsetsTable, session) -> None:
        try:
            with self.session() as session:
                session.add(handset_table_model)
                session.commit()
            logging.info("Handsets loaded successfully.")
        except Exception as e:
            session.rollback()
            logging.error(f"Error loading handsets: {e}")
        return
    
    def load_tariffs(self, tariff_table_models: List[TariffPlanTable], session) -> None:
        try:
            for tariff in tariff_table_models:
                session.add(tariff)
                session.flush()
                logging.info(f"Tariff {tariff.planOfferingCode} loaded successfully.")
            session.commit()       
        except Exception as e:
            logging.error(f"Error loading tariff {tariff.planOfferingCode}: {e}")
            session.rollback()
    
        

    def get_session(self):
        return self.session()

        

    
