import argparse
from pathlib import Path
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import os


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


    # Example arrays for correlation calculation
    array_1 = np.array([6246,6957,7273,7589,8451,9082,10443,11382,12041,12583,])
    array_2 = np.array([4.41667,4.75,5.08333,6.41667,6.25,9.5,10.3333,13.9167,20.0833,21.9167,])
    array_1_name = "Master's degrees awarded in Mathematics and statistics"
    array_2_name = "Google searches for 'why do i have a migraine'"

    # calculate correlations
    correlation, r_squared, p_value = calculate_correlation(array_1, array_2)

    # Write the correlation results to a file
    with (output_dir / "correlation_results.tex").open("x") as file:
        file.write(f"Correlation: {correlation}\n")
        file.write(f"R-squared: {r_squared}\n")
        file.write(f"P-value: {p_value}\n")


    # Make Plot
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Primary y-axis
    ax1.plot(array_1, 'o-', color='tab:blue', label=array_1_name)
    ax1.set_ylabel(array_1_name, color='tab:blue')
    ax1.set_ylim(6200, 12600)
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # Secondary y-axis
    ax2 = ax1.twinx()
    ax2.plot(array_2, 's--', color='tab:red', label=array_2_name)
    ax2.set_ylabel(array_2_name, color='tab:red')
    ax2.set_ylim(4, 22)
    ax2.tick_params(axis='y', labelcolor='tab:red')

    # X-axis
    ax1.set_xlabel("Index (e.g., Year or Observation Number)")
    plt.title("Comparison of Master's Degrees vs. Migraine Searches")
    plt.grid(True)
    fig.tight_layout()

# Save
    
    # Define path where to save the figure
    filename = "correlation_plot.png"
    save_path = os.path.join(output_dir, filename)

    # Save the plot
    plt.savefig(save_path)



def calculate_correlation(array1, array2):

    # Calculate Pearson correlation coefficient and p-value
    correlation, p_value = stats.pearsonr(array1, array2)

    # Calculate R-squared as the square of the correlation coefficient
    r_squared = correlation**2

    return correlation, r_squared, p_value    

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
