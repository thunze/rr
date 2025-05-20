{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
  };

  outputs =
    { nixpkgs, ... }:
    let
      supportedSystems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];

      forAllSystems =
        f:
        nixpkgs.lib.genAttrs supportedSystems (
          system:
          f {
            pkgs = import nixpkgs {
              inherit system;
            };
          }
        );
    in
    {
      packages = forAllSystems (
        { pkgs }:
        rec {
          paper = pkgs.stdenvNoCC.mkDerivation {
            name = "paper";
            src = ./.;

            buildInputs = with pkgs; [
              (texlive.combine {
                inherit (pkgs.texlive) scheme-minimal latex-bin latexmk;
              })
              (python312.withPackages (
                ps: with ps; [
                  numpy
                ]
              ))
            ];

            env = {
              TEXMFHOME = "./cache";
              TEXMFVAR = "./cache/texmf-var";
            };

            buildPhase = ''
              python ./code/main.py --data ./data/resolved --output ./paper/generated
              cd paper
              latexmk -interaction=nonstopmode -pdf -lualatex ./document.tex
            '';

            installPhase = ''
              mkdir -p $out
              cp document.pdf $out
            '';
          };

          default = paper;
        }
      );

      devShells = forAllSystems (
        { pkgs }:
        {
          default = pkgs.mkShell {

            packages = with pkgs; [
              bashInteractive
              git
              git-annex
            ];
          };
        }
      );

      formatter = forAllSystems ({ pkgs }: pkgs.nixfmt-tree);
    };
}
