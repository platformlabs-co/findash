{pkgs}: {
  deps = [
    pkgs.openssh
    pkgs.python312Packages.flake8
  ];
}
