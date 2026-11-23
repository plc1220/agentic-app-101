"""Build the Windows PCAI installer and its credential-free attendee ZIP.

Run from any directory: python tools/build_pcai_windows.py
Only Python's standard library is required.
"""
from pathlib import Path
import hashlib
import io
import json
import re
import stat
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "setup/pcai-windows"
OUT = ROOT / "downloads/PCAI_DeepSeek_Windows_AutoSetup.zip"
CA_SHA256 = "431955c40fbb33012ff7fe8babab41ffc60807531b7de68486f2621f62234e5e"
FILES = (
    "Start here.docx",
    "README.txt",
    "Setup PCAI.cmd",
    "OpenCode-PCAI.cmd",
    "pcai-settings.json",
    "pcai-ai-essentials-ca.crt",
)


def build_installer(source: str) -> bytes:
    """Use readable inline PowerShell without changing execution policies."""
    parts = []
    for line in source.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if '"' in line or "%" in line:
            raise ValueError("PowerShell source must not contain CMD quoting or expansion characters")
        parts.append(line if line.endswith("{") else line + ";")
    command = " ".join(parts)
    batch = (
        "@echo off\n"
        "setlocal EnableExtensions DisableDelayedExpansion\n"
        "title Setup PCAI DeepSeek\n"
        'set "PCAI_PACKAGE_DIR=%~dp0"\n'
        '"%SystemRoot%\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" '
        '-NoLogo -NoProfile -STA -Command "' + command + '"\n'
        'set "PCAI_RESULT=%ERRORLEVEL%"\n'
        "echo.\npause\nexit /b %PCAI_RESULT%\n"
    )
    if max(map(len, batch.splitlines())) >= 7600:
        raise ValueError("Installer exceeds the safe Windows CMD command length")
    return batch.replace("\n", "\r\n").encode("ascii")


def check_content(name: str, data: bytes) -> None:
    """Reject accidental credentials, private keys, and unresolved placeholders."""
    payloads = [data]
    if name.endswith(".docx"):
        with zipfile.ZipFile(io.BytesIO(data)) as doc:
            payloads.extend(doc.read(item) for item in doc.namelist())
    for payload in payloads:
        if re.search(rb"-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----", payload):
            raise ValueError("Private key found in package")
        if re.search(rb"eyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}", payload):
            raise ValueError("Possible API token found in package")
        if b"<PCAI_BASE_URL>" in payload or b"your_key_here" in payload:
            raise ValueError("Package still requires manual placeholder editing")


def main() -> None:
    source = (SOURCE / "Setup-PCAI.ps1").read_text(encoding="utf-8")
    (SOURCE / "Setup PCAI.cmd").write_bytes(build_installer(source))
    ca = (SOURCE / "pcai-ai-essentials-ca.crt").read_bytes()
    if hashlib.sha256(ca).hexdigest() != CA_SHA256:
        raise ValueError("Unexpected PCAI certificate")
    settings = json.loads((SOURCE / "pcai-settings.json").read_text(encoding="utf-8"))
    if settings["provider"]["pcai-deepseek"]["options"]["apiKey"] != "{file:./api-token}":
        raise ValueError("Settings must reference a local token file")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in FILES:
            data = (SOURCE / name).read_bytes()
            check_content(name, data)
            info = zipfile.ZipInfo("PCAI_DeepSeek_Windows_AutoSetup/" + name, date_time=(2026, 11, 23, 0, 0, 0))
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | (0o755 if name.endswith(".cmd") else 0o644)) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data)
    with zipfile.ZipFile(OUT) as archive:
        if archive.testzip() is not None or len(archive.namelist()) != len(FILES):
            raise ValueError("Archive integrity check failed")
    print("Built " + str(OUT))
    print("Included guide, setup, launcher, prefilled settings, and public CA. No token file is included.")


if __name__ == "__main__":
    main()
