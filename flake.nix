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
          # Generate the paper
          paper = pkgs.callPackage ./paper.nix { };
          paperAnnex = pkgs.callPackage ./paper.nix { customData = ./data/resolved; };

          # Check integrity of the generated paper
          verifyResult = pkgs.writeShellScriptBin "verify-result" ''
            cd ${paper}
            ${pkgs.hashdeep}/bin/hashdeep -alv -k ${./result.SUMS} -r .
          '';
          verifyResultAnnex = pkgs.writeShellScriptBin "verify-result-annex" ''
            cd ${paper}
            ${pkgs.hashdeep}/bin/hashdeep -alv -k ${./result.SUMS} -r .
          '';

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
