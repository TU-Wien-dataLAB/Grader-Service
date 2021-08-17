from nbconvert.exporters import notebook
from .models import GradeBookModel, Notebook, GradeCell, TaskCell, SolutionCell, SourceCell, Grade, Comment
from typing import Optional, Any, Union
import os
import json


class InvalidEntry(ValueError):
    pass


class MissingEntry(ValueError):
    pass

# TODO: add decorator to functions that sets dirty flag for methods and checks on __enter__
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
            self.data: dict = {"notebooks": dict()}
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
        kwargs = {k:v for k,v in kwargs.items() if k in set(Notebook.empty_dict().keys())}
        self.model.notebooks[name] = Notebook(name=name, **kwargs)

    def find_notebook(self, name: str) -> Notebook:
        """Find a particular notebook.
        Parameters
        ----------
        name:
            the name of the notebook
        Returns
        -------
        notebook : :class:`~Notebook`
        """
        try:
            return self.model.notebooks[name]
        except KeyError:
            raise MissingEntry()

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
        self.model.notebooks.pop(name, None)

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
        kwargs = {k:v for k,v in kwargs.items() if k in set(GradeCell.empty_dict().keys())}
        nb = self.find_notebook(notebook)
        nb.base_cells[name] = GradeCell(name=name, **kwargs)
        return nb.base_cells[name]

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
        nb = self.find_notebook(notebook)
        try:
            return [x for x in nb.grade_cells if x.name == name][0]
        except IndexError:
            raise MissingEntry()

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
        try:
            grade_cell = self.find_grade_cell(name, notebook)
        except MissingEntry:
            grade_cell = self.add_grade_cell(name, notebook, **kwargs)
        else:
            for attr in kwargs:
                setattr(grade_cell, attr, kwargs[attr])
        return grade_cell

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
        kwargs = {k:v for k,v in kwargs.items() if k in set(SolutionCell.empty_dict().keys())}
        nb = self.find_notebook(notebook)
        nb.base_cells[name] = SolutionCell(name=name, **kwargs)
        return nb.base_cells[name]

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
        nb = self.find_notebook(notebook)
        try:
            return [x for x in nb.solution_cells if x.name == name][0]
        except IndexError:
            raise MissingEntry()

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
        try:
            solution_cell = self.find_solution_cell(name, notebook)
        except MissingEntry:
            solution_cell = self.add_solution_cell(name, notebook, **kwargs)
        else:
            for attr in kwargs:
                setattr(solution_cell, attr, kwargs[attr])
        return solution_cell
    
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
        kwargs = {k:v for k,v in kwargs.items() if k in set(TaskCell.empty_dict().keys())}
        nb = self.find_notebook(notebook)
        nb.base_cells[name] = TaskCell(name=name, **kwargs)
        return nb.base_cells[name]
    
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
        nb = self.find_notebook(notebook)
        try:
            return [x for x in nb.task_cells if x.name == name][0]
        except IndexError:
            raise MissingEntry()
    
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
        try:
            task_cell = self.find_task_cell(name, notebook)
        except MissingEntry:
            task_cell = self.add_task_cell(name, notebook, **kwargs)
        else:
            for attr in kwargs:
                setattr(task_cell, attr, kwargs[attr])
        return task_cell
    
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
        kwargs = {k:v for k,v in kwargs.items() if k in set(SourceCell.empty_dict().keys())}
        nb = self.find_notebook(notebook)
        nb.src_cells[name] = SourceCell(name=name, **kwargs)
        return nb.src_cells[name]
    
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
        nb = self.find_notebook(notebook)
        try:
            return [x for x in nb.source_cells if x.name == name][0]
        except IndexError:
            raise MissingEntry()
    
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
        try:
            source_cell = self.find_source_cell(name, notebook)
        except MissingEntry:
            source_cell = self.add_source_cell(name, notebook, **kwargs)
        else:
            for attr in kwargs:
                setattr(source_cell, attr, kwargs[attr])
        return source_cell
    
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
    
    