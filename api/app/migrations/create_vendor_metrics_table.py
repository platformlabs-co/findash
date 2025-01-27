from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Float,
    UniqueConstraint,
)
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class VendorMetrics(Base):
    __tablename__ = "vendor_metrics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    vendor = Column(String)
    identifier = Column(String)
    month = Column(String)
    cost = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "vendor",
            "identifier",
            "month",
            name="uq_vendor_metrics_user_vendor_identifier_month",
        ),
    )


def upgrade(engine):
    Base.metadata.create_all(bind=engine, tables=[VendorMetrics.__table__])


def downgrade(engine):
    VendorMetrics.__table__.drop(engine)
