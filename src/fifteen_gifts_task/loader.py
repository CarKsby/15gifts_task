from sqlalchemy.orm import sessionmaker
from typing import List
import logging
from sqlalchemy import create_engine
from abc import ABC
from typing import Dict

from fifteen_gifts_task.models.table_models import Base, HandsetsTable, TariffPlanTable


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

    def load_handsets(self, handset_table_model: HandsetsTable) -> None:
        try:
            with self.session() as session:
                session.add(handset_table_model)
                session.commit()
            logging.info("Handsets loaded successfully.")
        except Exception as e:
            session.rollback()
            logging.error(f"Error loading handsets: {e}")
        return
    
    def get_session(self):
        return self.session()

        

    
