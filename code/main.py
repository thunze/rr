import argparse
import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


def generate_files(data_dir: Path, output_dir: Path):
    """Generate the necessary files for the paper.

    Args:
        data_dir: Path to the data directory.
        output_dir: Path to the output directory.
    """
    # Create the output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Read and clean data
    google_data, nces_data = read_data_and_clean_data(data_dir)

    # calculate correlations
    correlation, r_squared, p_value = calculate_correlation(nces_data, google_data)

    # Write the correlation results to a file
    save_correlation_results(correlation, r_squared, p_value, output_dir)

    # Create and save the plot
    create_and_save_plot(nces_data, google_data, output_dir)

    # calculate year-to-year changes
    nces_yearly_changes = np.diff(nces_data)
    google_yearly_changes = np.diff(google_data)

    # calculate correlations for year-to-year changes
    correlation_changes, r_squared_changes, p_value_changes = calculate_correlation(
        nces_yearly_changes, google_yearly_changes
    )

    # Write the year-to-year correlation results to a file
    save_correlation_results(
        correlation_changes,
        r_squared_changes,
        p_value_changes,
        output_dir,
        "yearly_changes_",
    )

    create_and_save_yearly_changes_plot(
        nces_yearly_changes, google_yearly_changes, output_dir
    )

    # Normalize the data
    nces_data_normalized = (nces_data - np.mean(nces_data)) / np.std(nces_data)
    google_data_normalized = (google_data - np.mean(google_data)) / np.std(google_data)
    # create linear regrsesion for comparison
    plot_linear_regression(nces_data_normalized, google_data_normalized, output_dir)


def read_data_and_clean_data(data_dir):
    """Read and clean data from the specified directory."""
    # Read the google trends "why do I have a migrane data" file into a DataFrame
    csv_file = data_dir / "multiTimeline.csv"
    google_data = pd.read_csv(csv_file, skiprows=1)
    if google_data.empty:
        raise ValueError("multiTimeline.csv is empty")

    # Read the nces master degree data file into a DataFrame
    excel_file = data_dir / "tabn323.10.xlsx"
    nces_data = pd.read_excel(
        excel_file, sheet_name="Digest 2022 Table 323.10", skiprows=2
    )
    if nces_data.empty:
        raise ValueError(
            "tabn323.10.xlsx is empty or does not contain the expected data"
        )

    ## Clean the google data
    # Rename the first column for easier access
    google_data.columns = ["Month", "Trend"]

    # Convert Month to datetime
    google_data["Month"] = pd.to_datetime(google_data["Month"], errors="coerce")
    google_data.dropna(subset=["Month"], inplace=True)

    # Extract the year
    google_data["Year"] = google_data["Month"].dt.year

    # Convert trend values to numeric
    google_data["Trend"] = pd.to_numeric(google_data["Trend"], errors="coerce")

    # Group by year and calculate the average
    yearly_avg = google_data.groupby("Year")["Trend"].mean().round(2)

    # Reshape to one row with years as columns
    cleaned_google_data = yearly_avg.to_frame().T

    # Save the cleaned google data to a CSV file (uncomment if needed)
    # path = data_dir / google_data_clean.csv"
    # cleaned_google_data.to_csv(path, index=False)

    ## Clean the nces data
    # Rename the first column for easier access
    nces_data.rename(columns={nces_data.columns[0]: "Field of study"}, inplace=True)

    # Filter for "Mathematics and statistics"
    math_stats_row = nces_data[
        nces_data["Field of study"] == "Mathematics and statistics"
    ]

    # Select columns for 2011-12 through 2020-21 (which correspond to columns 10
    # through 19)
    year_columns = list(range(10, 20))
    filtered_math_stats_by_year = math_stats_row[year_columns]

    # Rename the columns to include the year
    filtered_math_stats_by_year.columns = [int(year) for year in range(2012, 2022)]

    # Convert values to integers
    math_stats_values = filtered_math_stats_by_year.astype(int)

    # Save the cleaned nces data to a CSV file (uncomment if needed)
    # path = data_dir / "nces_data_clean.csv"
    # math_stats_values.to_csv(path, index=False)

    # convert to numpy array
    google_np = np.array(cleaned_google_data.iloc[0])
    nces_np = np.array(math_stats_values.iloc[0])

    # Print the numpy arrays (uncomment if needed)
    # print("Google Data (Numpy Array):", google_np)
    # print("NCES Data (Numpy Array):", nces_np)

    return google_np, nces_np


def save_correlation_results(
    correlation, r_squared, p_value, output_dir, filePrefix=""
):
    """Save the correlation results to files."""
    with (output_dir / f"{filePrefix}correlation_value.tex").open("w") as file:
        file.write(f"{correlation:.4f}")

    with (output_dir / f"{filePrefix}r_squared_value.tex").open("w") as file:
        file.write(f"{r_squared:.4f}")

    with (output_dir / f"{filePrefix}r_squared_percentage_value.tex").open("w") as file:
        file.write(f"{r_squared * 100:.2f}\\%")

    with (output_dir / f"{filePrefix}p_value.tex").open("w") as file:
        file.write(f"{p_value:.4g}")


def create_and_save_plot(array1, array2, output_dir):
    """Create and save a plot comparing two arrays."""
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Titles for correlation plots
    nces_data_name = "Master's degrees awarded in Mathematics and statistics"
    google_data_name = "Google searches for 'why do i have a migraine'"

    # Define the years corresponding to the data points
    years = np.arange(2012, 2012 + len(array1))

    # Primary y-axis
    ax1.plot(years, array1, "o-", color="tab:blue", label=nces_data_name)
    ax1.set_ylabel(nces_data_name, color="tab:blue")
    ax1.tick_params(axis="y", labelcolor="tab:blue")

    # Secondary y-axis
    ax2 = ax1.twinx()
    ax2.plot(years, array2, "s--", color="tab:red", label=google_data_name)
    ax2.set_ylabel(google_data_name, color="tab:red")
    ax2.tick_params(axis="y", labelcolor="tab:red")

    # X-axis
    ax1.set_xlabel("Year")
    ax1.set_xticks(years)
    ax1.set_xticklabels([str(year) for year in years])
    plt.title("Comparison of Master's Degrees and Google Searches")
    plt.grid(True)
    fig.tight_layout()

    # Save the plot
    filename = "correlation_plot.png"
    save_path = os.path.join(output_dir, filename)
    plt.savefig(save_path)

    # Close the plot to free up memory
    plt.close(fig)


def plot_linear_regression(x, y, output_dir, filename="linear_regression_plot.png"):
    index = np.arange(len(x))
    slope1, _, _, _, _ = stats.linregress(index, x)
    slope2, _, _, _, _ = stats.linregress(index, y)

    # save linear regression slope values
    with (output_dir / "nces_slope_value.tex").open("w") as file:
        file.write(f"{slope1:.4f}")
    with (output_dir / "google_slope_value.tex").open("w") as file:
        file.write(f"{slope2:.4f}")

    years = np.arange(2012, 2012 + len(x))

    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(years, x, "o-", color="tab:blue", label="Normalized NCES Data")
    ax1.plot(
        years,
        slope1 * index,
        color="tab:blue",
        linestyle="--",
        label="Normalized NCES Data Trend",
    )
    ax1.set_ylabel(
        (
            "Master's degrees awarded in Mathematics and statistics yearly changes\n"
            "(NCES Data)"
        ),
        color="tab:blue",
    )

    ax2 = ax1.twinx()
    ax2.plot(years, y, "o-", color="tab:red", label="Normalized Google searches")
    ax2.plot(
        years,
        slope2 * index,
        color="tab:red",
        linestyle="--",
        label="Normalized Google searches Trend",
    )
    ax2.set_ylabel(
        "Google searches for 'why do i have a migraine'\n(Google Searches)",
        color="tab:red",
    )

    ax1.set_xlabel("Year")
    ax1.set_title("Normalized Linear Regression Comparison")
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper center")

    plt.grid(True)
    fig.tight_layout()
    # Save the linear regression plot
    save_path = os.path.join(output_dir, filename)
    plt.savefig(save_path)
    # Close the plot to free up memory
    plt.close(fig)


def create_and_save_yearly_changes_plot(array1, array2, output_dir):
    """Create and save a plot comparing the yearly changse."""
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # years corresponding to the data points
    years = np.arange(2012, 2012 + len(array1))

    # Example arrays for correlation calculation
    nces_data_name = (
        "Master's degrees awarded in Mathematics and statistics yearly changes"
    )
    google_data_name = "Google searches for 'why do i have a migraine' yearly changes"

    # Primary y-axis
    ax1.plot(years, array1, "o-", color="tab:blue", label=nces_data_name)
    ax1.set_ylabel(nces_data_name, color="tab:blue")
    ax1.tick_params(axis="y", labelcolor="tab:blue")

    # Secondary y-axis
    ax2 = ax1.twinx()
    ax2.plot(years, array2, "s--", color="tab:red", label=google_data_name)
    ax2.set_ylabel(google_data_name, color="tab:red")
    ax2.tick_params(axis="y", labelcolor="tab:red")

    # X-axis
    ax1.set_xlabel("Year")
    plt.title("Comparison of yearly changes")
    plt.grid(True)
    fig.tight_layout()

    # Save the plot
    filename = "yearly_changes_correlation_plot.png"
    save_path = os.path.join(output_dir, filename)
    plt.savefig(save_path)

    # Close the plot to free up memory
    plt.close(fig)


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
