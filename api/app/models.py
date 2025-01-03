from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declared_attr
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import sqlalchemy

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    sub = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    name = Column(String, nullable=True)
    picture = Column(String, nullable=True)
    datadog_configurations = relationship(
        "DatadogAPIConfiguration", back_populates="user"
    )
    aws_configurations = relationship("AWSAPIConfiguration", back_populates="user")


class APIConfiguration(Base):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)

    @declared_attr
    def user_id(cls):
        return Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DatadogAPIConfiguration(APIConfiguration):
    __tablename__ = "datadog_api_configurations"

    app_key = Column(String)
    api_key = Column(String)
    user = relationship("User", back_populates="datadog_configurations")
    __table_args__ = (sqlalchemy.UniqueConstraint("user_id", name="uq_datadog_user"),)


class AWSAPIConfiguration(APIConfiguration):
    __tablename__ = "aws_api_configurations"

    aws_access_key_id = Column(String)
    aws_secret_access_key = Column(String)
    user = relationship("User", back_populates="aws_configurations")
    __table_args__ = (sqlalchemy.UniqueConstraint("user_id", name="uq_aws_user"),)
