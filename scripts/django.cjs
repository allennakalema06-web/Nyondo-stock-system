const { spawnSync } = require("node:child_process");
const { existsSync } = require("node:fs");
const { join } = require("node:path");
const root = join(__dirname, "..");
const local = join(root, ".venv", process.platform === "win32" ? "Scripts/python.exe" : "bin/python");
const python = process.env.PYTHON || (existsSync(local) ? local : "python");
const commands = process.argv[2] === "build"
  ? [["check"], ["collectstatic", "--noinput"]]
  : [["runserver", "127.0.0.1:8000", "--noreload"]];
for (const args of commands) {
  const result = spawnSync(python, ["manage.py", ...args], {
    cwd: join(root, "nyondo_stock"), stdio: "inherit", env: process.env
  });
  if (result.error) { console.error(result.error.message); process.exit(1); }
  if (result.status !== 0) process.exit(result.status || 1);
}
