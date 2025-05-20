import sys

from pathlib import Path


def generate_a_file():
    """Generate a file in the directory specified by the user as a command line
    argument.
    """
    # Create the output directory if it doesn't exist
    output_dir = Path(sys.argv[1])
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create a file in the output directory
    with (output_dir / "example.tex").open("x") as file:
        file.write("Some generated content\n")


if __name__ == "__main__":
    generate_a_file()
