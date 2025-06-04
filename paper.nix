{
  stdenvNoCC,
  python312,
  texlive,
  fetchzip,
  customData ? null,
}:

let
  dataDir =
    if customData != null then
      customData
    else
      fetchzip {
        url = "https://gist.github.com/thunze/d4e8052d2b9016ce7292ec5651a9509c/archive/40afb521f0b19a1cd803eccd369dfc2a76268f56.zip";
        hash = "sha256-19Jf8sivW/pO6hXT3QccrFw0TsNw+9T3OyafeJODWXk=";
      };
in
stdenvNoCC.mkDerivation {
  name = "paper";
  src = ./.;

  buildInputs = [
    (
      (texlive.combine {
        inherit (texlive) scheme-basic latex-bin latexmk;
      }).withPackages
      (
        ps: with ps; [
          csquotes
          float
        ]
      )
    )
    (python312.withPackages (
      ps: with ps; [
        matplotlib
        numpy
        openpyxl
        pandas
        scipy
      ]
    ))
  ];

  env = {
    TEXMFHOME = "./cache";
    TEXMFVAR = "./cache/texmf-var";
  };

  buildPhase = ''
    python ./code/main.py --data ${dataDir} --output ./paper/generated
    cd paper
    latexmk -interaction=nonstopmode -pdf -lualatex ./document.tex
  '';

  installPhase = ''
    mkdir -p $out
    cp document.pdf $out/migraines-math-degrees.pdf
  '';
}
