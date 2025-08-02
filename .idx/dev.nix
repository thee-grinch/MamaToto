{ pkgs, ... }: {
  packages = [
    pkgs.python3
    pkgs.nodejs_20
    pkgs.sqlite
    pkgs.vite
  ];

  idx = {
    extensions = [
      "ms-python.python"
      "Vue.volar"
    ];

    workspace = {
      onCreate = {
        # Create venv and install requirements if system packages are missing
        backend-setup = ''
          cd MamatotoAI/backend
          if ! python -c "import fastapi" 2>/dev/null; then
            python -m venv .venv
            . .venv/bin/activate
            pip install -r requirements.txt
          fi
        '';
        frontend-install = "cd MamatotoAI/frontend && npm install";
      };
      
      onStart = {
        # Activate venv if it exists, otherwise proceed (may fail if deps missing)
        backend-dev = ''
          cd MamatotoAI/backend
          if [ -d .venv ]; then
            . .venv/bin/activate
          fi
          uvicorn main:app --reload
        '';
        frontend-dev = "cd MamatotoAI/frontend && npm run dev";
      };
    };

    previews = {
      enable = true;
      previews = {
        web = {
          command = ["npm" "run" "dev" "--" "--port" "$PORT"];
          cwd = "MamatotoAI/frontend";
          manager = "web";
        };
      };
    };
  };
}