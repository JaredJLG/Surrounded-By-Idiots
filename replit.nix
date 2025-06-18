{ pkgs }: {
  deps = [
    pkgs.python311
    pkgs.poetry
  ];
  env = {
    LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
      pkgs.stdenv.cc.cc.lib
    ];
  };
}