
{pkgs}: {
  deps = [
    (pkgs.python313.override {
      packageOverrides = self: super: {
        python = super.python.override {
          version = "3.13.0a5";
        };
      };
    })
    pkgs.python312Packages.pip
    pkgs.python312Packages.flake8
    pkgs.openssh
  ];
}
