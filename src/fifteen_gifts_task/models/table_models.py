from sqlalchemy import Table, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Bridge table for many-to-many relationship between TariffPlan and Perk
tariff_extras = Table(
    "tariff_extras",
    Base.metadata,
    Column("tariff_id", ForeignKey("tariffs.id"), primary_key=True),
    Column("extras_id", ForeignKey("extras.id"), primary_key=True),
)


class HandsetsTable(Base):
    __tablename__ = "handsets"

    id = Column(Integer, primary_key=True)
    brand = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    averageRating = Column(Integer)  # Assuming rating is stored as an integer
    totalReviews = Column(Integer)
    inStock = Column(Integer)  
    isFiveGReady = Column(Integer)  
    isSwitchUpEligible = Column(Integer)  
    skuCode = Column(String, unique=True)

    handsetColours = relationship(
        "HandsetColourTable", back_populates="handsets", cascade="all, delete-orphan"
    )
    handsetTariffs = relationship(
        "TariffPlanTable", back_populates="handsets", cascade="all, delete-orphan"
    )


class HandsetColourTable(Base):
    __tablename__ = "handset_colours"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    hexCode = Column(String)
    handset_id = Column(Integer, ForeignKey("handsets.id"))

    handsets = relationship("HandsetsTable", back_populates="handsetColours")


class TariffPlanTable(Base):
    __tablename__ = "tariffs"

    id = Column(Integer, primary_key=True)
    planOfferingCode = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    totalUpfront = Column(Float, nullable=False)
    airtimeMrc = Column(Float, nullable=False) 
    deviceMrc = Column(Float, nullable=False)  
    api = Column(Float, nullable=False) 
    contractDuration = Column(Integer, nullable=False) 
    handset_id = Column(Integer, ForeignKey("handsets.id"))

    extras = relationship(
        "ExtraOffersTable", secondary=tariff_extras, back_populates="tariffs"
    )
    handsets = relationship("HandsetsTable", back_populates="handsetTariffs")


class ExtraOffersTable(Base):
    __tablename__ = "extras"

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    name = Column(String)

    tariffs = relationship(
        "TariffPlanTable", secondary=tariff_extras, back_populates="extras"
    )
