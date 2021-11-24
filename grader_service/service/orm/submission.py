from service.api.models import submission
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import false

from .base import Base, Serializable


class Submission(Base, Serializable):
    __tablename__ = "submission"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, nullable=False)
    auto_status = Column(
        Enum("pending", "not_graded", "automatically_graded"),
        default="not_graded",
        nullable=False,
    )
    manual_status = Column(Enum("not_graded", "manually_graded"))
    score = Column(Integer, nullable=True)
    assignid = Column(Integer, ForeignKey("assignment.id"))
    username = Column(String(255), ForeignKey("user.name"))
    commit_hash = Column(String(length=40), nullable=False)
    properties = Column(Text, nullable=True, unique=False)
    feedback_available = Column(Boolean, nullable=False)

    assignment = relationship("Assignment", back_populates="submissions")
    user = relationship("User", back_populates="submissions")

    @property
    def model(self) -> submission.Submission:
        return submission.Submission(
            id=self.id,
            submitted_at=None
            if self.date is None
            else (self.date.isoformat("T", "milliseconds") + "Z"),
            auto_status=self.auto_status,
            manual_status=self.manual_status,
            score=self.score,
            commit_hash=self.commit_hash,
            feedback_available=self.feedback_available,
        )
