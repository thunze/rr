# Reproducible Research

This repository contains the code for the fictional paper “Migraines and Math Degrees: A Spurious Love Story”, as well as the paper itself and all necessary files to generate a PDF version of the paper in a reproducible manner.

To build the paper, we use the [Nix package manager](https://nixos.org/download/) to ensure that the environment in which the paper is built is consistent across different systems. The tools and packages required in the build process are fetched automatically by the Nix package manager from the [Nixpkgs](https://github.com/NixOS/nixpkgs) repository, which is the official package repository for Nix. In particular, these tools include LaTeX for typesetting the paper and Python, along with several Python packages, for processing the data and generating plots.

Nix also aids in achieving bit-for-bit reproducibility of the generated PDF file, meaning that the same source code and data produces exactly the same PDF file every time it is built. This is particularly important for scientific papers, where reproducibility is a key aspect of the research process.

Building the paper requires some data files, which are fetched from the internet during the build process. The data includes [Google Trends](https://trends.google.com/trends/) data for specific search terms, as well as data from the [National Center for Education Statistics (NCES)](https://nces.ed.gov/). Both data sources have been made available separately in a [GitHub Gist](https://gist.github.com/thunze/d4e8052d2b9016ce7292ec5651a9509c). This data can be fetched either automatically by Nix during the build process or manually using [git-annex](https://git-annex.branchable.com/), which is a tool for managing large files in Git repositories.

A pre-built version of this paper is available [here](https://github.com/thunze/rr/blob/1.1/migraines-math-degrees.pdf).

To get started with reproducing the paper, you can follow the instructions below.

## Requirements

- [Git](https://git-scm.com/)
  - Last tested using [version 2.49.0](https://mirrors.edge.kernel.org/pub/software/scm/git/)
- [Nix, the package manager](https://nixos.org/download/)
  - Last tested using [version 2.25.3](https://releases.nixos.org/?prefix=nix/nix-2.25.3/)

### Platform requirements

Building the paper has been tested on the following platforms:

- **Linux**: Ubuntu 22.04 LTS, NixOS 25.05
- **macOS**: macOS 13.6.3 (Ventura)
- **Windows**: Windows 11 with WSL (Windows Subsystem for Linux) and Ubuntu 22.04 LTS

If you are using macOS or Linux, you are already set up to run the commands in this guide, as Nix is natively supported on these platforms. Simply open a terminal and continue with the instructions for installing Git and Nix below.

If you are using Windows, you will need to install WSL (Windows Subsystem for Linux) and set up a Linux distribution (e.g., Ubuntu) to run the commands in this guide. This is because Nix is not natively supported on Windows as Nix relies on a Unix-like environment.

#### Setting up WSL with Ubuntu on Windows

You must be running Windows 11 version 2004 and higher (Build 19041 and higher) or Windows 11 to use the following instructions to install WSL and set up a Linux distribution.

1. Open a Windows Terminal or PowerShell as an **administrator** by searching for _Windows Terminal_ or _PowerShell_ in the Start menu, right-clicking on it, and selecting _Run as administrator_.
2. Enter the `wsl --install -d Ubuntu-22.04` command to install WSL (if it isn't already installed) and set up the Ubuntu Linux distribution.
3. If WSL isn't already installed, this command will also enable the required Windows features and download the necessary components to run WSL. In that case, it will prompt you to restart your computer to complete the installation. After the restart, open _Ubuntu_ from the Start menu to complete the setup.
4. After the installation is complete and Ubuntu has been launched, WSL will prompt you to enter a username and password for your new Linux user account. Choose a username and password that you will remember, as you will use these to log in to your WSL environment. Note that this account is not related to your Windows user account.
5. Once the setup is complete, you can use the Linux shell to run commands.

These commands were taken from the [WSL installation guide](https://docs.microsoft.com/en-us/windows/wsl/install). Please refer to that guide for more information or if you encounter any issues.

In the following sections of this guide, please follow the instructions for Linux if you are using WSL, as the commands are the same for both WSL and a native Linux installation.

### Installing Git

Please head to the [Git downloads page](https://git-scm.com/downloads) and select your platform. Follow the instructions provided there to install Git.

> [!TIP]
> If you are using **WSL**, you can install Git by running the following command in your Linux shell: `sudo apt install git`. You may need to enter your Linux user password to allow the installation to proceed.

### Installing Nix

Nix can be installed using the following command:

```sh
sh <(curl --proto '=https' --tlsv1.2 -L https://nixos.org/nix/install)
```

This will download and run the Nix installation script, which will guide you through the installation process. You may need to enter your password to allow the installation to proceed. For more information on installing Nix, see the [Nix installation guide](https://nix.dev/manual/nix/stable/quick-start).

#### Enabling Nix flakes

Building the paper also requires you to have [Nix flakes](https://nixos.wiki/wiki/Flakes) enabled. To do this, you need to add the following line to your Nix configuration file (at `/etc/nix/nix.conf` or `~/.config/nix/nix.conf`):

```sh
experimental-features = nix-command flakes
```

This can be done automatically by running the following commands in your terminal:

```sh
sudo mkdir -p /etc/nix # this creates the /etc/nix directory
echo 'experimental-features = nix-command flakes' | sudo tee -a /etc/nix/nix.conf # creates nix.conf file and adds line
```

You're all set! You can now proceed to build the paper using Nix as described below. 🎉

## Building the paper

There are two main ways to build the paper:

1. Using data fetched from the internet using Nix.
2. Using data fetched from the internet using [git-annex](https://git-annex.branchable.com/).

### 1. Using Nix

Simply run the following command:

```sh
nix build github:thunze/rr/1.1#paper
```

You can find the built paper in `result/migraines-math-degrees.pdf`.

> [!TIP]
> If you are using **WSL** and you want to view the PDF file you can install a pdf viewer (e.g. [xdg-open](https://freedesktop.org/wiki/Software/xdg-utils/)) or wsl utilities ([wslu](https://github.com/wslutilities/wslu)) to view it using your windows pdf viewer. To install either of these you first have to run `sudo apt-get update` to update your local package index. Afterwards you can install xdg-utils using `sudo apt install xdg-utils` or wslu using `sudo apt install wslu`.
>- If you installed xdg-utils you can then open the pdf file by navigating to the `result` directory and running `open migraines-math-degrees.pdf`.
>- if you installed wslu you can open the `result` directory in your windows explorer by navigating to the `result` directory by running `wslview .`

### 2. Using git-annex

First clone the repository and navigate to the cloned directory:

```sh
git clone --branch 1.1 https://github.com/thunze/rr.git
# Or using SSH:
# git clone --branch 1.1 git@github.com:thunze/rr.git
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

- `nix run github:thunze/rr/1.1#verifyResult` if you used method 1 (pure Nix build).
- `nix run .#verifyResultAnnex` if you used method 2 (Nix build with data fetched via git-annex).

If the verification passes, you should see output similar to the following:

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
