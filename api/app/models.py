
from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, CheckConstraint, DateTime, Float, JSON
from sqlalchemy.orm import relationship
from app.helpers.database import Base

class VendorMetric(Base):
    __tablename__ = "vendor_metrics"

    id = Column(Integer, primary_key=True, index=True)
    vendor_type = Column(String(50), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    usage_data = Column(JSON)
    total_cost = Column(Float)
    api_configuration_id = Column(Integer, ForeignKey("api_configurations.id"), nullable=False)
    api_configuration = relationship("APIConfiguration", back_populates="metrics")

APIConfiguration.metrics = relationship("VendorMetric", back_populates="api_configuration")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    sub = Column(String, unique=True, index=True)
    api_configurations = relationship("APIConfiguration", back_populates="user", cascade="all, delete-orphan")

class APIConfiguration(Base):
    __tablename__ = "api_configurations"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="api_configurations")

    __mapper_args__ = {
        'polymorphic_identity': 'api_configuration',
        'polymorphic_on': type
    }

class DatadogAPIConfiguration(APIConfiguration):
    __tablename__ = "datadog_api_configurations"

    id = Column(Integer, ForeignKey("api_configurations.id"), primary_key=True)
    app_key = Column(String)
    api_key = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'datadog',
    }

    __table_args__ = (
        CheckConstraint(
            '(app_key IS NOT NULL) OR (api_key IS NOT NULL)',
            name='check_at_least_one_key'
        ),
    )
