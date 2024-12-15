
{pkgs}: {
  deps = [
    pkgs.python312
    pkgs.python312Packages.pip
    pkgs.python312Packages.flake8
    pkgs.openssh
  ];
}
