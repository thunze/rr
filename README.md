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

You can find the built paper in `result/migraines-math-degrees.pdf`.

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

You can find the built paper in `result/migraines-math-degrees.pdf`.

## Verifying the build

This paper aims to be bit-for-bit reproducible, meaning that the same source code and data should produce the same output every time it is built.

To verify this, you can check the output of the build (currently, the PDF file) against known good hashes in `result.SUMS` by running:

- `nix build github:thunze/rr#verifyResult` if you used method 1 (pure Nix build).
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

