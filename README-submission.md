# Reproducible Research Submission

- Finished paper: https://github.com/thunze/rr/blob/1.1/migraines-math-degrees.pdf
- Data: https://gist.github.com/thunze/d4e8052d2b9016ce7292ec5651a9509c
- Repository: https://github.com/thunze/rr/blob/1.1

## Repository contents

- `code/main.py`: Code for data processing and analysis
- `data/`: Directory containing placeholders for downloaded data files (will be populated automatically)
- `paper/`: Directory containing the LaTeX source code for the paper
- `LICENSE`: License of all source code files (see https://github.com/thunze/rr/blob/1.1/README.md#license for details)
- `LICENSE-paper`: License of the paper itself (see https://github.com/thunze/rr/blob/1.1/README.md#license for details)
- `README.md`: Overview of the repository and instructions for building and verifying the paper
- `README-submission.md`: This file, containing information relevant for the submission
- `flake.nix`: Nix flake code exporting the Nix derivations for building and verifying the paper, as well as a Nix shell for convenient development
- `flake.lock`: Nix flake lock file accompanying the `flake.nix` file, referencing the exact revision of Nixpkgs (https://github.com/NixOS/nixpkgs) used in `flake.nix`
- `migraines-math-degrees.pdf`: A pre-built version of the paper, i.e., the output of the build process
- `paper.nix`: Nix derivation for building the finished paper, referenced in `flake.nix`
- `result.SUMS`: File containing the expected hashes of the built paper, used for automatic verification of the built paper
- Files not directly relevant to the paper: `.envrc` (direnv configuration), `.gitignore` (to prevent committing certain files to the repository)
