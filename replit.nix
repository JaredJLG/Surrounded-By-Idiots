{ pkgs }: {
  deps = [
    # Match the python version in pyproject.toml
    pkgs.python311
    # Ensure poetry is always available
    pkgs.poetry
    pkgs.libxml2
    pkgs.libxslt
    pkgs.zlib
  ];
}
