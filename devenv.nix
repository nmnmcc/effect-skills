{
  pkgs,
  ...
}:

{
  packages = [
    pkgs.git
    pkgs.curl
    pkgs.nodejs_22
    (pkgs.python312.withPackages (pythonPackages: [
      pythonPackages.pyyaml
      pythonPackages.markdown-it-py
    ]))
  ];

  env = {
    DISABLE_TELEMETRY = "1";
    NPM_CONFIG_FUND = "false";
    NPM_CONFIG_UPDATE_NOTIFIER = "false";
    PYTHONDONTWRITEBYTECODE = "1";
  };

  tasks = {
    "check:skills" = {
      exec = "python scripts/validate-skills.py";
    };
  };

  enterTest = ''
    npm test
  '';
}
