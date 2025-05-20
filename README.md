# Reproducible Research

## Requirements

- An operating system / platform that supports Nix (Linux, macOS, Windows via WSL)
  - Last tested on [Ubuntu 22.04 LTS](https://releases.ubuntu.com/jammy/)
- The [Nix package manager](https://nixos.org/download/)
  - Last tested using [version 2.25.3](https://releases.nixos.org/?prefix=nix/nix-2.25.3/)
- [Git](https://git-scm.com/)
  - Last tested using [version 2.49.0](https://mirrors.edge.kernel.org/pub/software/scm/git/)

Building the paper also requires you to have [Nix flakes](https://nixos.wiki/wiki/Flakes) enabled. To do this, add the following line to your Nix configuration file (at `~/.config/nix/nix.conf` or `/etc/nix/nix.conf`):

```conf
experimental-features = nix-command flakes
```

## Building the paper

There are two main ways to build the paper:

1. Using data fetched from the internet using Nix.
2. Using data fetched from the internet using [git-annex](https://git-annex.branchable.com/).

**TODO:** Add commit revision

### 1. Using Nix

Simply run the following command:

```sh
nix build github:thunze/rr#paper
```

You can find the built paper in `result/document.pdf`.

### 2. Using git-annex

First clone the repository and navigate to the cloned directory:

```sh
git clone https://github.com/thunze/rr.git
# Or using SSH:
# git clone git@github.com:thunze/rr.git
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

You can find the built paper in `result/document.pdf`.
