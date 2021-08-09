from dataclasses import asdict, dataclass
from typing import Any, Optional, Type, List
from enum import Enum

class BaseModel:
    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> Type["BaseModel"]:
        return cls(**d)


@dataclass
class IDMixin:
    id: str


@dataclass
class NameMixin:
    name: str


@dataclass
class NotebookRelashionship:
    notebook_id: str


@dataclass
class CellRelashionship:
    cell_id: str


class Grade(BaseModel, IDMixin, NotebookRelashionship, CellRelashionship):
    auto_score: float
    manual_score: float
    extra_credit: float
    needs_manual_grade: bool

    @property
    def score(self) -> float:
        """
        The overall score, computed automatically from the
        :attr:`~api.models.Grade.auto_score` and :attr:`~api.models.Grade.manual_score`
        values. If neither are set, the score is zero. If both are set, then the
        manual score takes precedence. If only one is set, then that value is used
        for the score
        """
        if self.manual_score is None and self.auto_score is None:
            return 0.0
        elif self.manual_score is None:
            return self.auto_score
        elif self.auto_score is None:
            return self.manual_score
        else:
            return self.manual_score


@dataclass
class Comment(BaseModel, IDMixin, NotebookRelashionship, CellRelashionship):
    auto_comment: str
    manual_comment: str

    @property
    def comment(self) -> Optional[str]:
        if self.manual_comment is None:
            return self.auto_comment
        else:
            return self.manual_comment


@dataclass
class BaseCell(BaseModel, IDMixin, NameMixin, NotebookRelashionship):
    type: str  # type of cell
    grade: Grade  # we can have only one grade
    comment: Comment  # we can have only one comment since we only process a single notebook


class CellType(Enum):
    "code"
    "markdown"

@dataclass
class GradedMixin:
    max_score: float
    cell_type: CellType

# TODO: finish creating models

@dataclass
class Notebook(BaseModel, IDMixin, NameMixin):
    kernelspec: str
    _base_cells: List[BaseCell]