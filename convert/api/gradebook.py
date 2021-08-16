from models import GradeBookModel, Notebook, GradeCell, TaskCell, SolutionCell, SourceCell, Grade, Comment
from typing import Optional, Any, Union
import os
import json


class InvalidEntry(ValueError):
    pass


class MissingEntry(ValueError):
    pass


class Gradebook:
    """
    The gradebook object to interface with the JSON output file of a conversion.
    Should only be used as a context manager when changing the data.
    """

    def __init__(self, dest_json: str) -> None:
        self.json_file: str = dest_json
        if os.path.isfile(self.json_file):
            with open(self.json_file, "r") as f:
                self.data: dict = json.load(f)
        else:
            os.makedirs(os.path.dirname(self.json_file), exist_ok=True)
            self.data: dict = dict()
            with open(self.json_file, "w") as f:
                json.dump(self.data, f)
        self.model: GradeBookModel = GradeBookModel.from_dict(self.data)

    def __enter__(self) -> "Gradebook":
        return self

    def __exit__(
        self,
        exc_type: Optional[Any],
        exc_value: Optional[Any],
        traceback: Optional[Any],
    ) -> None:
        with open(self.json_file, "w") as f:
            json.dump(self.model.to_dict(), f)

    # Notebooks

    def add_notebook(self, name: str, **kwargs: dict) -> Notebook:
        """Add a new notebook to the :class:`~GradeBookModel`.
        Parameters
        ----------
        name:
            the name of the new notebook
        `**kwargs`
            additional keyword arguments for the :class:`~Notebook` object
        Returns
        -------
        notebook : :class:`~Notebook`
        """
        raise NotImplementedError()

    def find_notebook(self, name: str) -> Notebook:
        """Find a particular notebook.
        Parameters
        ----------
        name:
            the name of the notebook
        Returns
        -------
        notebook : :class:`~nNotebook`
        """
        raise NotImplementedError()

    def update_or_create_notebook(self, name: str, **kwargs):
        """Update an existing notebook, or create it if it doesn't exist.
        Parameters
        ----------
        name : string
            the name of the notebook
        `**kwargs`
            additional keyword arguments for the :class:`~Notebook` object
        Returns
        -------
        notebook : :class:`~nNotebook`
        """
        raise NotImplementedError()

    def remove_notebook(self, name: str):
        """Deletes an existing notebook from the gradebook.
        Parameters
        ----------
        name : string
            the name of the notebook to delete
        """
        raise NotImplementedError()

    # Grade cells

    def add_grade_cell(self, name: str, notebook: str, **kwargs: dict) -> GradeCell:
        """Add a new grade cell to an existing notebook.
        Parameters
        ----------
        name:
            the name of the new grade cell
        notebook:
            the name of an existing notebook
        `**kwargs`
            additional keyword arguments for :class:`~GradeCell`
        Returns
        -------
        grade_cell
        """
        raise NotImplementedError()

    def find_grade_cell(self, name: str, notebook: str) -> GradeCell:
        """Find a grade cell in a particular notebook.
        Parameters
        ----------
        name:
            the name of the grade cell
        notebook:
            the name of the notebook
        Returns
        -------
        grade_cell
        """
        raise NotImplementedError()

    def find_graded_cell(self, name: str, notebook: str) -> Union[GradeCell, TaskCell]:
        """Find a graded cell in a particular notebook. This can be either a GradeCell or a TaskCell.
        Parameters
        ----------
        name:
            the name of the grade cell
        notebook:
            the name of the notebook
        Returns
        -------
        grade_cell
        """
        raise NotImplementedError()

    def update_or_create_grade_cell(
        self, name: str, notebook: str, **kwargs: dict
    ) -> GradeCell:
        """Update an existing grade cell in a notebook, or create the grade cell if it does not exist.
        Parameters
        ----------
        name:
            the name of the grade cell
        notebook:
            the name of the notebook
        `**kwargs`
            additional keyword arguments for :class:`~GradeCell`
        Returns
        -------
        grade_cell
        """
        raise NotImplementedError()

    # Solution cells

    def add_solution_cell(
        self, name: str, notebook: str, **kwargs: dict
    ) -> SolutionCell:
        """Add a new solution cell to an existing notebook.
        Parameters
        ----------
        name:
            the name of the new solution cell
        notebook:
            the name of an existing notebook
        `**kwargs`
            additional keyword arguments for :class:`~SolutionCell`
        Returns
        -------
        solution_cell : :class:`~SolutionCell`
        """
        raise NotImplementedError()

    def find_solution_cell(self, name: str, notebook: str) -> SolutionCell:
        """Find a solution cell in a particular notebook.
        Parameters
        ----------
        name : string
            the name of the solution cell
        notebook : string
            the name of the notebook
        Returns
        -------
        solution_cell : :class:`~SolutionCell`
        """
        raise NotImplementedError()

    def update_or_create_solution_cell(
        self, name: str, notebook: str, **kwargs: dict
    ) -> SolutionCell:
        """Update an existing solution cell in a notebook, or create the solution cell if it does not exist.
        Parameters
        ----------
        name:
            the name of the solution cell
        notebook:
            the name of the notebook
        `**kwargs`
            additional keyword arguments for :class:`~SolutionCell`
        Returns
        -------
        solution_cell
        """
        raise NotImplementedError()
    
    # Task cells

    def add_task_cell(self, name: str, notebook: str, **kwargs: dict) -> TaskCell:
        """Add a new task cell to an existing notebook.
        Parameters
        ----------
        name:
            the name of the new task cell
        notebook:
            the name of an existing notebook
        `**kwargs`
            additional keyword arguments for :class:`~TaskCell`
        Returns
        -------
        task_cell
        """
        raise NotImplementedError()
    
    def find_task_cell(self, name: str, notebook: str) -> TaskCell:
        """Find a task cell in a particular notebook.
        Parameters
        ----------
        name : string
            the name of the task cell
        notebook : string
            the name of the notebook
        Returns
        -------
        task_cell : :class:`~TaskCell`
        """
        raise NotImplementedError()
    
    def update_or_create_task_cell(self, name: str, notebook: str, **kwargs) -> TaskCell:
        """Update an existing task cell in a notebook, or create the task cell if it does not exist.
        Parameters
        ----------
        name : string
            the name of the task cell
        notebook : string
            the name of the notebook
        `**kwargs`
            additional keyword arguments for :class:`~TaskCell`
        Returns
        -------
        task_cell : :class:`~TaskCell`
        """
        raise NotImplementedError()
    
    # Source cell

    def add_source_cell(self, name: str, notebook: str, **kwargs: dict) -> SourceCell:
        """Add a new source cell to an existing notebook.
        Parameters
        ----------
        name : string
            the name of the new source cell
        notebook : string
            the name of an existing notebook
        `**kwargs`
            additional keyword arguments for :class:`~SourceCell`
        Returns
        -------
        source_cell : :class:`~SourceCell`
        """
        raise NotImplementedError()
    
    def find_source_cell(self, name: str, notebook: str) -> SourceCell:
        """Find a source cell in a particular notebook.
        Parameters
        ----------
        name:
            the name of the source cell
        notebook:
            the name of the notebook
        Returns
        -------
        source_cell : :class:`~SourceCell`
        """
        raise NotImplementedError()
    
    def update_or_create_source_cell(self, name: str, notebook: str, **kwargs: dict) -> SourceCell:
        """Update an existing source cell in a notebook of an assignment, or
        create the source cell if it does not exist.
        Parameters
        ----------
        name:
            the name of the source cell
        notebook:
            the name of the notebook
        `**kwargs`
            additional keyword arguments for :class:`~SourceCell`
        Returns
        -------
        source_cell
        """
        raise NotImplementedError()
    
    # Grades

    def find_grade(self, grade_cell: str, notebook: str) -> Grade:
        """Find a particular grade in a notebook.
        Parameters
        ----------
        grade_cell:
            the name of a grade or task cell
        notebook:
            the name of a notebook
        Returns
        -------
        grade
        """
        raise NotImplementedError()
    
    def find_grade_by_id(self, grade_id: str) -> Grade:
        """Find a grade by its unique id.
        Parameters
        ----------
        grade_id : string
            the unique id of the grade
        Returns
        -------
        grade : :class:`~Grade`
        """
        raise NotImplementedError()
    
    def find_comment(self, solution_cell: str, notebook: str) -> Comment:
        """Find a particular comment in a notebook.
        Parameters
        ----------
        solution_cell:
            the name of a solution or task cell
        notebook:
            the name of a notebook
        assignment:
            the name of an assignment
        student:
            the unique id of a student
        Returns
        -------
        comment
        """
        raise NotImplementedError()
    
    def find_comment_by_id(self, comment_id: str) -> Comment:
        """Find a comment by its unique id.
        Parameters
        ----------
        comment_id : string
            the unique id of the comment
        Returns
        -------
        comment : :class:`~Comment`
        """
        raise NotImplementedError()
    
    