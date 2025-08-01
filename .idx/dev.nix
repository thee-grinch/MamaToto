# .idx/dev.nix

{ pkgs, ... }: {
  channel = "stable-24.05";

  packages = [
    pkgs.python312
    pkgs.python312Packages.pip
    pkgs.python312Packages.uvicorn
    pkgs.python312Packages.setuptools
    pkgs.python312Packages.wheel
  ];

  env = {
    PYTHONUNBUFFERED = "1";
  };

  idx = {
    extensions = [
      "ms-python.python"
    ];

    previews = {
      enable = true;
      previews = {
        backend = {
          command = [
            "sh" "-c"
            "cd mamatoto-backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT"
          ];
          manager = "web";
          env = {
            PORT = "8000";
          };
        };
      };
    };

    workspace = {
      onCreate = {
        install-deps = ''
          cd mamatoto-backend
          pip install --upgrade pip setuptools wheel
          if [ -f requirements.txt ]; then
            pip install -r requirements.txt
          fi
        '';
      };
      onStart = { };
    };
  };
}
