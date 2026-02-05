from sqlalchemy import Column, Integer, String, Float, DECIMAL, TIMESTAMP, DateTime, func, ForeignKey, CheckConstraint, Text
from sqlalchemy.orm import relationship
from config import Base
from datetime import datetime


class TransactionModel(Base):
    """SQLAlchemy Transaction model"""
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, index=True)
    passbook_id = Column(Integer, ForeignKey("passbook.id", ondelete="CASCADE"))
    txn_type = Column(String(10), nullable=False)  # debit or credit
    amount = Column(DECIMAL(15, 2), nullable=False)
    description = Column(Text)
    txn_date = Column(TIMESTAMP, default=datetime.utcnow)
    reference_no = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        CheckConstraint("txn_type IN ('debit','credit')", name="check_txn_type"),
    )

   # passbook = relationship("Passbook", back_populates="transactions")


    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "passbook_id": self.passbook_id,
            "txn_type": self.txn_type,
            "amount": self.amount,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
