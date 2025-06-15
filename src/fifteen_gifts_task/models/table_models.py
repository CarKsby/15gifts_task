from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class HandsetsTable(Base):
    __tablename__ = "handsets"

    id = Column(Integer, primary_key=True)
    brand = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    averageRating = Column(Integer) 
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
    handsetId = Column(Integer, ForeignKey("handsets.id"))

    handsets = relationship("HandsetsTable", back_populates="handsetColours")


class TariffPlanTable(Base):
    __tablename__ = "tariffs"

    id = Column(Integer, primary_key=True)
    planOfferingCode = Column(String, nullable=False)
    name = Column(String, nullable=False)
    totalUpfront = Column(Float, nullable=False)
    airtimeMrc = Column(Float, nullable=False)
    deviceMrc = Column(Float, nullable=False)
    api = Column(Float, nullable=False)
    contractDurationMonths = Column(Integer, nullable=False)
    handsetId = Column(Integer, ForeignKey("handsets.id"))

    handsets = relationship("HandsetsTable", back_populates="handsetTariffs")
