import argparse
from pathlib import Path


def generate_files(data_dir: Path, output_dir: Path):
    """Generate the necessary files for the paper.
    
    Args:
        data_dir: Path to the data directory.
        output_dir: Path to the output directory.
    """
    # Read some data (just an example)
    with (data_dir / "multiTimeline.csv").open("r") as file:
        data = file.read()
        if not data:
            raise ValueError("multiTimeline.csv is empty")

    # Create the output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create a file in the output directory
    with (output_dir / "example.tex").open("x") as file:
        file.write(f"Some generated content: {data[:25]}")


def main():
    """Main function, executed when the script is run."""
    parser = argparse.ArgumentParser(description="Generate files for the paper.")
    parser.add_argument("-d", "--data", help="where to find the data", required=True)
    parser.add_argument(
        "-o", "--output", help="where to put the generated files", required=True
    )
    args = parser.parse_args()
    generate_files(Path(args.data), Path(args.output))


if __name__ == "__main__":
    main()
