"""Checks for the actual attendee package and installer source.

Run: python -m unittest discover -s tests -p test_pcai_windows_package.py
Set PCAI_PWSH to a Microsoft PowerShell executable for syntax and file-write checks.
"""
from pathlib import Path
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("pcai_builder", ROOT / "tools/build_pcai_windows.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class WindowsPackageTests(unittest.TestCase):
    def test_package_is_reproducible_and_contains_no_token_file(self):
        with contextlib.redirect_stdout(io.StringIO()):
            builder.main()
            first = builder.OUT.read_bytes()
            builder.main()
        self.assertEqual(first, builder.OUT.read_bytes())
        with zipfile.ZipFile(builder.OUT) as archive:
            self.assertIsNone(archive.testzip())
            expected = {"PCAI_DeepSeek_Windows_AutoSetup/" + name for name in builder.FILES}
            self.assertEqual(set(archive.namelist()), expected)
            for name in archive.namelist():
                self.assertNotIn("api-token", Path(name).name)
                builder.check_content(name, archive.read(name))

    def test_prefilled_config_and_certificate(self):
        config = json.loads((builder.SOURCE / "pcai-settings.json").read_text())
        options = config["provider"]["pcai-deepseek"]["options"]
        self.assertEqual(options["apiKey"], "{file:./api-token}")
        self.assertEqual(options["baseURL"], "https://deepseekv41flash.project-user-shahriln.serving.htp-ai-ai-application.awanheitech.local/v1")
        self.assertEqual(config["model"], "pcai-deepseek/deepseek-ai/deepseek-v4.1-flash")
        self.assertEqual(hashlib.sha256((builder.SOURCE / "pcai-ai-essentials-ca.crt").read_bytes()).hexdigest(), builder.CA_SHA256)

    def test_launcher_and_installer_boundaries(self):
        source = (builder.SOURCE / "Setup-PCAI.ps1").read_text()
        generated = builder.build_installer(source)
        self.assertEqual(generated, (builder.SOURCE / "Setup PCAI.cmd").read_bytes())
        self.assertNotIn(b"\n", generated.replace(b"\r\n", b""))
        for prohibited in [b"-ExecutionPolicy", b"-EncodedCommand", b"Invoke-Expression", b"Set-ExecutionPolicy"]:
            self.assertNotIn(prohibited, generated)
        launch = (builder.SOURCE / "OpenCode-PCAI.cmd").read_text()
        self.assertIn('set "OPENCODE_CONFIG=%PCAI_DIR%\\pcai.json"', launch)
        self.assertIn('set "NODE_TLS_REJECT_UNAUTHORIZED=1"', launch)
        self.assertNotRegex(launch.lower(), r"\b(taskkill|setx)\b")
        labels = set(re.findall(r"^:([a-z_]+)\s*$", launch, re.M))
        for target in re.findall(r"\bgoto ([a-z_]+)", launch, re.I):
            self.assertIn(target, labels)

    def test_power_shell_source_generated_command_and_real_file_updates(self):
        pwsh = os.environ.get("PCAI_PWSH") or shutil.which("pwsh") or shutil.which("powershell")
        if not pwsh:
            self.skipTest("PowerShell not installed; set PCAI_PWSH to run parser and filesystem checks")
        generated = builder.build_installer((builder.SOURCE / "Setup-PCAI.ps1").read_text()).decode("ascii")
        command = next(line.split('-Command "', 1)[1][:-1] for line in generated.splitlines() if '-Command "' in line)
        with tempfile.TemporaryDirectory(prefix="pcai-setup-test-") as temp:
            inline = Path(temp) / "inline.ps1"
            inline.write_text(command)
            run = subprocess.run([
                pwsh, "-NoLogo", "-NoProfile", "-File", str(ROOT / "tests/pcai_file_updates.ps1"),
                "-SourcePath", str(builder.SOURCE / "Setup-PCAI.ps1"),
                "-InlinePath", str(inline), "-Scratch", str(Path(temp) / "writes"),
            ], capture_output=True, text=True, timeout=30)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)


if __name__ == "__main__":
    unittest.main()
