

# coding: utf-8

import os
import traceback

from nbformat import current_nbformat
from nbformat import read as orig_read
from nbformat import write as orig_write
from traitlets import Bool

from grader_service.convert.nbgraderformat import (
    MetadataValidator,
    SchemaTooNewError,
    ValidationError,
    write,
)
from grader_service.convert.utils import find_all_notebooks
from grader_service.convert.converters.baseapp import ConverterApp

aliases = {
    "log-level": "Application.log_level",
}
flags = {}


class UpdateApp(ConverterApp):

    name = u"update"
    description = u"Update nbgrader notebook metadata"

    aliases = aliases
    flags = flags

    validate = Bool(True, help="whether to validate metadata after updating it").tag(
        config=True
    )

    examples = """
        nbgrader stores metadata in the JSON source of the notebooks. Previously,
        we did not do a good job of validating whether this metadata was
        correctly formatted or not. Starting in version 0.4.0 of nbgrader, we
        are explicitly validating this metadata. This will require that you
        update the metadata in your old nbgrader notebooks to be consistent
        with what nbgrader expects.

        The `nbgrader update` command performs this metadata update for you
        easily. All you need to do is point it at a directory, and it will
        find all notebooks in that directory and update them to have the
        correct metadata:

            # update notebooks rooted in the current directory
            nbgrader update .

            # update notebooks rooted in the `class_files` directory
            nbgrader update class_files/

        Alternately, you can open all your notebooks with the "Create Assignment"
        toolbar and re-save them from the notebook interface. But, it will be
        more efficient to run the `nbgrader update` command to get them all in
        one fell swoop.
        """

    def start(self):
        super(UpdateApp, self).start()

        if len(self.extra_args) < 1:
            self.fail(
                "No notebooks or directories given. Usage:\n\n"
                "nbgrader update <NOTEBOOK>\n"
                "nbgrader update <DIRECTORY>\n"
            )

        notebooks = set()
        for name in self.extra_args:
            if not os.path.exists(name):
                self.fail("No such file or directory: {}".format(name))
            elif os.path.isdir(name):
                notebooks.update(
                    [os.path.join(name, x) for x in find_all_notebooks(name)]
                )
            elif not name.endswith(".ipynb"):
                self.log.warning("{} is not a notebook, ignoring".format(name))
            else:
                notebooks.add(name)

        notebooks = sorted(list(notebooks))
        for notebook in notebooks:
            self.log.info("Updating metadata for notebook: {}".format(notebook))
            nb = orig_read(notebook, current_nbformat)
            nb = MetadataValidator().upgrade_notebook_metadata(nb)
            if self.validate:
                try:
                    write(nb, notebook)
                except ValidationError:
                    self.log.error(traceback.format_exc())
                    self.fail(
                        "Notebook '{}' failed to validate, metadata is corrupted".format(
                            notebook
                        )
                    )
                except SchemaTooNewError:
                    self.log.error(traceback.format_exc())
                    self.fail(
                        (
                            "The notebook '{}' uses a newer version "
                            "of the nbgrader metadata format. Please update your version of "
                            "nbgrader to the latest version to be able to use this notebook."
                        ).format(notebook)
                    )
            else:
                orig_write(nb, notebook)
