
{pkgs}: {
  deps = [
    (pkgs.python312.override {
      packageOverrides = self: super: {
        python = super.python.override {
          version = "3.12.2";
        };
      };
    })
    pkgs.python312Packages.pip
    pkgs.python312Packages.flake8
    pkgs.openssh
  ];
}
