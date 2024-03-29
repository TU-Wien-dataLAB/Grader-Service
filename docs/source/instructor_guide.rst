Instructor Guide
=================

After installation and configuration of the grader labextension and service you should
be able to access the frontend interface of the extension.
The labextension consists of two launchers.
The assignment launcher opens a window where students can pull and submit their
given assignments.
The course management launcher opens a dashboard
for instructors where you can add, edit and delete assignments.
The course management launcher is only visible if the current user is at least
a tutor in one lecture.

.. image:: _static/assets/images/launcher.png
    :alt: launcher window

.. note::
    If you do not see the launcher items, it may be the case that extensions might be disabled in JupyterLab.
    You can find how to enable extensions `here <https://jupyterlab.readthedocs.io/en/stable/user/extensions.html#managing-extensions-using-the-extension-manager>`_.
    Another reason might be that the grader service is not running. However, there will be a warning if this is the case.

Create Your First Assignment
-----------------------------
Before students can access the notebooks, an assignment must be created.
To access this feature, open the course management dashboard and navigate to desired lecture:

.. image:: _static/assets/images/courses.png
    :alt: course management list

| The course management table lists all assignments in the chosen lecture and lets you easily manage them:

.. image:: _static/assets/images/assignments.png
    :alt: assignment list

| By pressing on the "+ NEW" button on top of the assignment list, instructors can add new assignments to the lecture:

.. image:: _static/assets/images/add_assignment.png
    :alt: add assignment dialog

Working With Assignments
------------------------
Once an assignment has been created it can be opened, which will display the overview window.
In the overview window of the assignment, you will find many ways to monitor, grade and extend the current assignment.

.. image:: _static/assets/images/overview_user_guide.png
    :alt: overview window

Files
--------------------

Every assignment includes two crucial directories.
The **source directory** contains the source notebooks which instructors create for their assignment.
The **release directory** contains the release versions of the notebooks, which are the converted source notebooks and is used as a preview of what the student version of the notebook looks.
To view these directories, use the files card in the overview window of the assignment.
By switching between source and release file viewer, the extension will convert the source notebooks to their release versions.

.. image:: _static/assets/images/file_view.png
    :alt: file view

.. note::
    Just the source notebooks and files should be edited! Changes to files in the release directory will be lost when generating the files again.

The grader service and labextension use git to support the collaborative creation of assignments. Also, it provides a simple way to distribute the files to the students.
Notebooks can be added by either using the "Create a new notebook" button or by copying files directly into the correct source directory via the file browser on left-hand side.

The source directory can also be revealed in the JupyterLab file browser or be opened in a terminal window.

Creating a Notebook for an Assignment
--------------------------------------

Up until now, no files have been added to the assignment. To have tasks for students to work on, notebooks have to be added to the assignment.
As mentioned previously, we can either add a notebook from the file view or create it using the JupyterLab launcher.

.. image:: _static/assets/images/creation_mode.png
    :width: 500
    :alt: creation mode
    :align: center

| For notebooks which are in the source directory, a creation mode can be enabled in the notebook toolbar. It adds widgets around notebook cells that can be used to control the function of the code cell.

Grader Cell Types:

- Readonly
    This cell is locked and editing is disabled.
- Autograded answer
    This cell contains the code for the solution of a task.
    It has to be surrounded by  ``BEGIN SOLUTION`` and ``END SOLUTION`` directives as comments around the actual solution code.
    Due to the directives, the code will be replaced by placeholder code such as ``raise NotImplementedError()``.
    Also, a hint can be given to students and solutions can be commented while grading.

    .. image:: _static/assets/images/autograded_answer.png
        :width: 500
        :alt: autograded answer
        :align: center

    .. warning::
        If the ``BEGIN SOLUTION`` and ``END SOLUTION`` directives are omitted, the solution code will end up in the released files!

- Autograded tests
    This cell contains the test cases to test the auto-graded answer given by students.
    These may be ``assert`` statements that check the implemented code.
    Invalid solutions have to lead to an exception.

    .. note::
        Part or all of the tests can be hidden with ``BEGIN HIDDEN TESTS`` and ``END HIDDEN TESTS`` directives.

    .. image:: _static/assets/images/autograded_test.png
        :width: 500
        :alt: autograded test
        :align: center

    Tests can also always be hidden with the use of ``BEGIN ALWAYS HIDDEN TESTS`` and ``END ALWAYS HIDDEN TESTS`` directives. This means that students won't see tests which were run in the generated feedback. This behavior might be desired for **automatic** and **fully automatic** grading scenarios, where students receive feedback as soon as they submit their work and can continue working on their assignments.
    
    .. image:: _static/assets/images/always_hidden_tests.png
        :width: 500
        :alt: allways hidden test
        :align: center

    The following image shows both an always hidden and a hidden test cell in the feedback view. For always hidden tests, only the points reached in the submission are shown, whereas for hidden tests, the run tests are also displayed.
   
    .. image:: _static/assets/images/student_feedback_always_hidden_tests.png
        :alt: feedback for always hidden tests
        

- Manual graded answer
    This cell type supports free-form answers from students.
    They should not be tested with automatic tests but are intended to be manually graded.
    The cells can be configured to either be code or markdown cells, so students can either implement code or answer in text.

    .. image:: _static/assets/images/manual_answer.png
        :width: 500
        :alt: manual answer
        :align: center



Customizing Assignment Creation with grader_config.py
=====================================================

Instructors have the ability to customize the grading process using a configuration file named ``grader_config.py``. This file should reside in the same directory as the assignment notebooks you wish to grade.

How to Use ``grader_config.py``
-------------------------------

1. **Create a ``grader_config.py`` File**
    Create this file in the directory that houses your assignment notebooks.

.. image:: _static/assets/images/grader_convert.png
    :alt: grader convert file

2. **Edit the Configurations**
    Open the ``grader_config.py`` file in a text editor and edit the configurations. Here are some commonly used options:

    - **Customizing the Code Stub for Solution Cells**
        Normally, solution cells are replaced with ``raise NotImplementedError()``. Modify this default behavior like so:

        .. code-block:: python

            c.ClearSolutions.code_stub = { 'python': "# The stage is yours\nraise NotImplementedError('No Answer Given!')" }


    - **Changing Delimiters for Hidden Tests**
        By default, the grader identifies hidden tests using "BEGIN HIDDEN TESTS" and "END HIDDEN TESTS". You can modify these by setting the following:

        .. code-block:: python

            c.ClearHiddenTests.begin_test_delimiter = "HIDE TEST START"
            c.ClearHiddenTests.end_test_delimiter = "HIDE TEST END"


3. **Save the Configuration**
    After setting your configurations, save the ``grader_config.py`` file.

This way the grader service would generate following assignment:

.. image:: _static/assets/images/grader_convert_example.png
    :width: 500
    :alt: grader convert result
    :align: center

From following assignment notebook:

.. image:: _static/assets/images/grader_convert_result.png
    :width: 500
    :alt: grader convert example
    :align: center

Applying Custom Configurations
------------------------------
Once the ``grader_config.py`` file is saved in the appropriate directory, the grader service will automatically use these configurations during the creation process.

Sample ``grader_config.py``
---------------------------
Here is a sample ``grader_config.py`` template for reference:

.. code-block:: python

    # Grader Convert Configuration File

    # -------------------------------------------------
    # ClearSolutions Configuration
    # -------------------------------------------------

    # `code_stub` replaces the content of solution cells with a language-specific code snippet.
    # Instructors can override these placeholders with the code snippets of their choice.
    c.ClearSolutions.code_stub = {
        'python': "# YEEETE\nraise NotImplementedError()",  # Placeholder for Python solution cells
        'matlab': "% YOUR CODE HERE\nerror('No Answer Given!')",  # Placeholder for MATLAB solution cells
        'octave': "% YOUR CODE HERE\nerror('No Answer Given!')",  # Placeholder for Octave solution cells
        # ... (More languages)
    }

    # -------------------------------------------------
    # ClearAlwaysHiddenTests Configuration
    # -------------------------------------------------

    # Delimiters for always hidden utilities.
    # Blocks of code between these delimiters will always be hidden in the notebook.
    c.ClearAlwaysHiddenTests.begin_util_delimeter = "BEGIN ALWAYS HIDDEN UTILS"  # Start delimiter
    c.ClearAlwaysHiddenTests.end_util_delimeter = "END ALWAYS HIDDEN UTILS"  # End delimiter

    # -------------------------------------------------
    # ClearHiddenTests Configuration
    # -------------------------------------------------

    # Delimiters for hidden tests.
    # Blocks of code between these delimiters will be hidden in the notebook.
    c.ClearHiddenTests.begin_test_delimeter = "BEGIN HIDDEN TESTS"  # Start delimiter
    c.ClearHiddenTests.end_test_delimeter = "END HIDDEN TESTS"  # End delimiter

    # -------------------------------------------------
    # ClearMarkScheme Configuration
    # -------------------------------------------------

    # Delimiters for the mark scheme.
    # Blocks of text between these delimiters describe the marking scheme.
    c.ClearMarkScheme.begin_mark_scheme_delimeter = "BEGIN MARK SCHEME"  # Start delimiter
    c.ClearMarkScheme.end_mark_scheme_delimeter = "END MARK SCHEME"  # End delimiter

    # -------------------------------------------------
    # IncludeHeaderFooter Configuration
    # -------------------------------------------------

    # Header and Footer files to be included at the top and bottom of each notebook.
    c.IncludeHeaderFooter.header = "header.ipynb"  # Header notebook file
    c.IncludeHeaderFooter.footer = "footer.ipynb"  # Footer notebook file

    # -------------------------------------------------
    # LimitOutput Configuration
    # -------------------------------------------------

    # Limit the number of lines and traceback lines in the output cells.
    c.LimitOutput.max_lines = 1000  # Max number of lines in output
    c.LimitOutput.max_traceback = 100  # Max number of traceback lines

    # -------------------------------------------------
    # LockCells Configuration
    # -------------------------------------------------

    # Options for locking cells in the notebook to prevent editing.
    c.LockCells.lock_solution_cells = True  # Lock solution cells
    c.LockCells.lock_grade_cells = True  # Lock grade cells
    c.LockCells.lock_readonly_cells = True  # Lock readonly cells
    c.LockCells.lock_all_cells = False  # Lock all cells in the notebook (overrides above settings)


Assignment Lifecycle
---------------------

.. image:: _static/assets/images/assignment_status.png
    :width: 400
    :alt: assignment status
    :align: center

| An assignment can have 3 states that can be switched between and represent the lifecycle of the assignment.

- Edit
    When first created, the assignment is in "Edit mode", where the assignment files can be added and edited.
    In this stage, the assignment is not visible to students. However, when an instructor opens the student view ("Assignments" card in launcher), it will be displayed to them.
- Released
    The assignment is released to students and the students can work on it.
    The released files are identical to the files in the release directory at the time of the release.
    It is possible to undo the release and publish a new release. However, some students may have already pulled the old release.
    In this case the students might have to reset their files and might loose progress, which has to be communicated.
    In general, a re-release should be avoided.

    .. warning::
        Revoking a released assignment may lead to diverging states of student files and submissions that fail auto-grading.

- Completed
    The assignment is over and cannot be worked on anymore and new submissions will be rejected, but it is still visible.
    This state can be revoked without any consideration and will return to a released state.


Grading Assignments
--------------------

To grade student submissions navigate to submissions tab:

.. image:: _static/assets/images/submission_grading.png
    :alt: submission grading


| Submissions can be selected from the list and actions can be performed on the submissions.

Grader Service supports batch auto-grading and batch feedback generation of several submissions.
Naturally, submissions have to be manually graded individually.

Generally, submissions have to be auto-graded first before anything else can be done.
If manual grading is not needed or not wanted, it can be skipped.
The last step is feedback generation, at which point students will see their results.


Auto-Grading Behavior
-----------------------

In the edit and creation menu for an assignment, it is possible to select the auto-grading behavior for the assignment.
It specifies the action taken when a user submits an assignment.

- No Automatic Grading
    No action is taken when users submit the assignment.
- Automatic Grading (Recommended)
    The assignment is being auto-graded as soon as the user submits the assignment.
    This means that submissions in the grading view are always auto-graded.
- Fully Automatic Grading
    The assignment is auto-graded and feedback is generated as soon as the student submits their assignment.
    This requires that no manually graded cells are part of the assignment.

.. image:: _static/assets/images/autograding_behavior.png
    :width: 350
    :alt: autograding behavior
    :align: center

