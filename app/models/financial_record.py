from sqlalchemy import Column, Integer, ForeignKey, DateTime, Numeric, String, Boolean, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.models.user import Base

class RecordType(str, enum.Enum):
    income = "income"
    expense = "expense"

class FinancialRecord(Base):
    __tablename__ = "financial_records"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))

    amount = Column(Numeric(10, 2), nullable=False)
    type = Column(Enum(RecordType), nullable=False)

    date = Column(DateTime, nullable=False)
    notes = Column(String)

    is_deleted = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    category = relationship("Category", back_populates="records")