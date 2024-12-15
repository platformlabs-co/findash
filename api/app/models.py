from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    CheckConstraint,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from app.helpers.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    sub = Column(String, unique=True, index=True)
    api_configurations = relationship(
        "APIConfiguration", back_populates="user", cascade="all, delete-orphan"
    )


class APIConfiguration(Base):
    __tablename__ = "api_configurations"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="api_configurations")

    __table_args__ = (
        CheckConstraint("type IN ('datadog')", name="check_valid_type"),
        UniqueConstraint("user_id", "type", name="unique_user_type"),
    )

    __mapper_args__ = {
        "polymorphic_identity": "api_configuration",
        "polymorphic_on": type,
    }


class DatadogAPIConfiguration(APIConfiguration):
    """DatadogAPIConfiguration model for storing API configuration."""
    
    __tablename__ = "datadog_api_configurations"

    id = Column(Integer, ForeignKey("api_configurations.id"), primary_key=True)
    app_key_secret_id = Column(String)
    api_key_secret_id = Column(String)

    __mapper_args__ = {"polymorphic_identity": "datadog"}

    __table_args__ = (
        CheckConstraint(
            "(app_key_secret_id IS NOT NULL) OR (api_key_secret_id IS NOT NULL)",
            name="check_at_least_one_key",
        ),
    )
