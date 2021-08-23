from converters.autograde import AutogradeApp
from converters.generate_solution import GenerateSolutionApp
from converters.baseapp import (
    ConverterApp,
    base_converter_aliases,
    base_converter_flags,
)
from converters.generate_assignment import GenerateAssignmentApp
from textwrap import dedent


aliases = {}
aliases.update(base_converter_aliases)
aliases.update({})

flags = {}
flags.update(base_converter_flags)
flags.update({})


class GraderConverter(ConverterApp):

    name = u"grader-converter"
    description = u"Convert notebooks to different formats"
    version = ConverterApp.__version__

    aliases = aliases
    flags = flags

    subcommands = dict(
        generate_assignment=(
            GenerateAssignmentApp,
            dedent(
                """
                Create the student version of an assignment. Intended for use by
                instructors only.
                """
            ).strip(),
        ),
        generate_solution=(
            GenerateSolutionApp,
            dedent(
                """
                Generates the solution for the given assignment.
                """
            ).strip(),
        ),
        autograde=(
            AutogradeApp,
            dedent(
                """
                Autograde submitted assignments. Intended for use by instructors
                only.
                """
            ).strip(),
        ),
    )


def main():
    GraderConverter.launch_instance()


if __name__ == "__main__":
    main()