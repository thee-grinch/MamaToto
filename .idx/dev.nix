{ pkgs, ... }: {
  channel = "stable-24.05";

  packages = [
    (pkgs.python312.withPackages (ps: with ps; [
      pip
      setuptools
      wheel
      fastapi
      uvicorn
      sqlalchemy
      pydantic
      python-jose
      passlib
      python-dateutil
      alembic
      gunicorn
      httpx
      pytest
      pytest-asyncio
    ]))
  ];

  env = {
    PYTHONUNBUFFERED = "1";
    PYTHONPATH = "./mamatoto-backend";  # Add this to ensure Python can find your modules
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
            "cd mamatoto-backend && python -m pip install -e . && uvicorn app.main:app --host 0.0.0.0 --port $PORT"
          ];
          manager = "web";
          env = {
            PORT = "8000";
          PYTHONPATH = "./mamatoto-backend";
          };
        };
      };
    };

    workspace = {
      onCreate = {
        install-extra = ''
          cd mamatoto-backend
          python -m pip install --upgrade pip setuptools wheel
          python -m pip install pydantic-settings python-multipart
          python -m pip install -e .
          if [ -f requirements.txt ]; then
            python -m pip install -r requirements.txt
          fi
        '';
      };
    };
  };
}