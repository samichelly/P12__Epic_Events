import sys
from pathlib import Path

parent_path = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_path))

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Boolean,
    Text,
    Date,
    DECIMAL,
    Enum,
    Sequence,
)
import bcrypt
import enum
from datetime import date
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from CRM_EPIC_EVENTS.settings import DATABASE_URL

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class User_role(enum.Enum):
    sales = "sales"
    support = "support"
    management = "management"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=True)
    _password = Column("password", String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(Enum(User_role), name="user_role", default="support")
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext_password):
        hashed_password = bcrypt.hashpw(
            plaintext_password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        self._password = hashed_password

    def check_password(self, plaintext_password):
        return bcrypt.checkpw(
            plaintext_password.encode("utf-8"), self._password.encode("utf-8")
        )


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    creation_date = Column(Date, default=date.today, nullable=False)
    last_contact_date = Column(
        Date, default=date.today, onupdate=date.today, nullable=False
    )
    sales_contact_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    sales_contact = relationship("User", backref="customer_sales")

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    remaining_amount = Column(DECIMAL(10, 2), nullable=False)
    creation_date = Column(Date, default=date.today, nullable=False)
    is_signed = Column(Boolean, default=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    management_contact_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    customer = relationship("Customer", backref="contracts")
    management_contact = relationship("User", backref="contract_management")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    event_name = Column(String, nullable=False)
    event_date_start = Column(DateTime, nullable=False)
    event_date_end = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)
    attendees = Column(Integer, nullable=False)
    notes = Column(Text, nullable=False)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    support_contact_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    contract = relationship("Contract", backref="event_contract")
    support_contact = relationship("User", backref="event_support")


Base.metadata.create_all(engine)
