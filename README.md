# Reproducible Research

## Requirements

- An operating system / platform that supports Nix (Linux, macOS, Windows via WSL)
  - Last tested on [Ubuntu 22.04 LTS](https://releases.ubuntu.com/jammy/)
- The [Nix package manager](https://nixos.org/download/)
  - Last tested using [version 2.25.3](https://releases.nixos.org/?prefix=nix/nix-2.25.3/)
- [Git](https://git-scm.com/)
  - Last tested using [version 2.49.0](https://mirrors.edge.kernel.org/pub/software/scm/git/)

Nix can be installed using the following command:

```sh
sh <(curl --proto '=https' --tlsv1.2 -L https://nixos.org/nix/install)
```

For more information on installing Nix, see the [Nix installation guide](https://nix.dev/manual/nix/stable/quick-start).

Building the paper also requires you to have [Nix flakes](https://nixos.wiki/wiki/Flakes) enabled. To do this, add the following line to your Nix configuration file (at `~/.config/nix/nix.conf` or `/etc/nix/nix.conf`):

```conf
experimental-features = nix-command flakes
```

If the file does not exist, you will need to create it first.

## Building the paper

There are two main ways to build the paper:

1. Using data fetched from the internet using Nix.
2. Using data fetched from the internet using [git-annex](https://git-annex.branchable.com/).

### 1. Using Nix

Simply run the following command:

```sh
nix build github:thunze/rr/1.0#paper
```

You can find the built paper in `result/migraines-math-degrees.pdf`.

### 2. Using git-annex

First clone the repository and navigate to the cloned directory:

```sh
git clone --branch 1.0 https://github.com/thunze/rr.git
# Or using SSH:
# git clone --branch 1.0 git@github.com:thunze/rr.git
cd rr
```

Activate the provided Nix shell to get access to git-annex:

```sh
nix develop
```

Then, run the following commands to fetch the data using git-annex and prepare it for the build:

```sh
git annex get
cp -Lr data/*.* data/resolved
```

Finally, build the paper:

```sh
nix build .#paperAnnex
```

You can find the built paper in `result/migraines-math-degrees.pdf`.

## Verifying the build

This paper aims to be bit-for-bit reproducible, meaning that the same source code and data should produce the same output every time it is built.

To verify this, you can check the output of the build (currently, the PDF file) against known good hashes in `result.SUMS` by running:

- `nix build github:thunze/rr/1.0#verifyResult` if you used method 1 (pure Nix build).
- `nix build .#verifyResultAnnex` if you used method 2 (Nix build with data fetched using git-annex).

If the verification is successful, you should see the following output:

```
hashdeep: Audit passed
          Files matched: 1
Files partially matched: 0
            Files moved: 0
        New files found: 0
  Known files not found: 0
```

## Rationale for using Nix

Nix is used in this project to ensure that the build environment is reproducible and consistent across different systems. It allows us to specify exact versions of dependencies and tools, which helps avoid issues related to differing software versions or configurations. [Nixpkgs](https://github.com/NixOS/nixpkgs) also applies specific patches to the TeX Live distribution it provides to ensure that built PDFs are reproducible, which aids in achieving bit-for-bit reproducibility.

## License

This project is licensed as follows:

- All source code files in this repository are licensed under the [The Unlicense](https://unlicense.org/) (SPDX identifier: `Unlicense`). See the `LICENSE` file for the full license text.
- The generated paper is licensed under the [CC0 1.0 Universal license](https://creativecommons.org/publicdomain/zero/1.0/) (SPDX identifier: `CC0-1.0`). See the `LICENSE-paper` file for the full license text.
- The licensing of the Google Trends data is described in the [Google Terms of Service](https://web.archive.org/web/20250604045244/https://policies.google.com/terms).
- The NCES data is placed in the public domain by the U.S. Department of Education, as described in 17 U.S. Code § 105.
