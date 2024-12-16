
{pkgs}: {
  deps = [
    pkgs.black
    pkgs.python311
    pkgs.python311Packages.pytest
    pkgs.python311Packages.flake8
  ];
}
