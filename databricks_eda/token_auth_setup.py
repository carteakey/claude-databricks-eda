#!/usr/bin/env python3
"""
Databricks Authentication Setup

Uses the Databricks SDK to read credentials from ~/.databrickscfg (or environment
variables) and writes them to .env for use by DatabricksQueryClient.

For interactive OAuth (browser-based login), the new Go-based Databricks CLI is used:
  brew install databricks/tap/databricks
  databricks auth login --host <host>

Usage:
    databricks-eda-setup [--refresh-token] [--test-connection]
    python -m databricks_eda.token_auth_setup [--refresh-token] [--test-connection]
"""

import os
import shutil
import subprocess
import sys
import argparse
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


def _find_env_file(workspace_root: Path) -> Path:
    """Return the .env path (workspace root)."""
    return workspace_root / ".env"


def _load_env(workspace_root: Path) -> None:
    """Load .env from workspace root if it exists."""
    env_file = workspace_root / ".env"
    if env_file.exists():
        load_dotenv(env_file, override=True)


def _read_host_from_env(workspace_root: Path) -> Optional[str]:
    """Return DATABRICKS_HOST from .env, or None."""
    _load_env(workspace_root)
    host = os.getenv("DATABRICKS_HOST")
    if not host:
        print("❌ DATABRICKS_HOST not set in .env — please add it first.")
        print("   Example: DATABRICKS_HOST=https://my-workspace.cloud.databricks.com")
    return host


def _read_http_path_from_env(workspace_root: Path) -> Optional[str]:
    """Return DATABRICKS_HTTP_PATH from .env, or None."""
    _load_env(workspace_root)
    http_path = os.getenv("DATABRICKS_HTTP_PATH")
    if not http_path:
        print("❌ DATABRICKS_HTTP_PATH not set in .env — please add it first.")
        print("   Example: DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/<warehouse-id>")
    return http_path


class DatabricksTokenSetup:
    """Manage Databricks authentication using the official databricks-sdk."""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or Path.cwd()
        self.env_file = _find_env_file(self.workspace_root)
        self.host: Optional[str] = None
        self.http_path: Optional[str] = None

    def _ensure_credentials_in_env(self) -> bool:
        """Read host and http_path from .env. Return False if missing."""
        self.host = _read_host_from_env(self.workspace_root)
        self.http_path = _read_http_path_from_env(self.workspace_root)
        return bool(self.host and self.http_path)

    # ------------------------------------------------------------------
    # Interactive OAuth via new Go-based Databricks CLI
    # ------------------------------------------------------------------

    def _find_go_cli(self) -> Optional[str]:
        """Return path to the new Go-based Databricks CLI, or None."""
        cli = shutil.which("databricks")
        if cli:
            try:
                result = subprocess.run(
                    [cli, "version"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                if "Databricks CLI" in result.stdout or "Databricks CLI" in result.stderr:
                    return cli
            except Exception:
                pass
        return None

    def run_oauth_login(self) -> bool:
        """Run interactive OAuth browser login via the Go Databricks CLI."""
        cli = self._find_go_cli()
        if not cli:
            print("⚠️  New Databricks CLI (Go) not found on PATH.")
            print("   Install it with:  brew install databricks/tap/databricks")
            print("   Then re-run:      databricks auth login --host <your-host>")
            print()
            print("   Alternatively, set DATABRICKS_ACCESS_TOKEN in .env directly.")
            return False

        if not self.host:
            print("❌ No host set — cannot run OAuth login.")
            return False

        print(f"🔑 Running OAuth login via Databricks CLI...")
        print(f"   This will open a browser window for authentication.")
        try:
            result = subprocess.run(
                [cli, "auth", "login", "--host", self.host],
                timeout=300,
            )
            if result.returncode == 0:
                print("✅ OAuth login completed.")
                return True
            else:
                print(f"❌ OAuth login failed (exit code {result.returncode}).")
                return False
        except subprocess.TimeoutExpired:
            print("❌ OAuth login timed out.")
            return False
        except Exception as exc:
            print(f"❌ OAuth login error: {exc}")
            return False

    # ------------------------------------------------------------------
    # Token extraction via databricks-sdk
    # ------------------------------------------------------------------

    def extract_token(self) -> Optional[str]:
        """Extract access token using the Databricks SDK Config."""
        try:
            from databricks.sdk.config import Config  # type: ignore[import]
        except ImportError:
            print("❌ databricks-sdk not installed. Run: pip install databricks-sdk")
            return None

        if not self.host:
            return None

        print(f"🔍 Reading credentials for {self.host} via databricks-sdk...")
        try:
            config = Config(host=self.host)
            token = config.token
            if token:
                print(f"✅ Token found ({len(token)} chars).")
                return token
            else:
                print("⚠️  SDK returned no token for this host.")
                print("   Make sure ~/.databrickscfg has an entry for this host,")
                print("   or run: databricks auth login --host <your-host>")
                return None
        except Exception as exc:
            print(f"❌ Could not read token from SDK: {exc}")
            return None

    # ------------------------------------------------------------------
    # .env file management
    # ------------------------------------------------------------------

    def update_env_file(self, access_token: str) -> bool:
        """Write the access token (and connection details) into .env."""
        print(f"📝 Updating {self.env_file}...")
        try:
            env_content: dict = {}
            if self.env_file.exists():
                with open(self.env_file) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            key, value = line.split("=", 1)
                            env_content[key] = value

            hostname = self.host or ""
            for prefix in ("https://", "http://"):
                hostname = hostname.removeprefix(prefix)

            env_content.update(
                {
                    "DATABRICKS_HOST": self.host or "",
                    "DATABRICKS_SERVER_HOSTNAME": hostname,
                    "DATABRICKS_HTTP_PATH": self.http_path or "",
                    "DATABRICKS_ACCESS_TOKEN": access_token,
                    "DATABRICKS_AUTH_TYPE": "token",
                }
            )

            with open(self.env_file, "w") as f:
                for key, value in env_content.items():
                    f.write(f"{key}={value}\n")

            print(f"✅ {self.env_file} updated.")
            return True
        except Exception as exc:
            print(f"❌ Failed to update .env: {exc}")
            return False

    # ------------------------------------------------------------------
    # Connection test
    # ------------------------------------------------------------------

    def test_connection(self) -> bool:
        """Test connection using DatabricksQueryClient."""
        print("🧪 Testing connection...")
        try:
            from databricks_eda.databricks_query import DatabricksQueryClient

            client = DatabricksQueryClient(env_path=self.env_file, debug=True)
            result = client.execute_query("SELECT 1 AS test_value", "Connection Test")
            if result is not None and not result.empty:
                print("✅ Connection successful!")
                return True
            print("❌ Connection test returned no results.")
            return False
        except Exception as exc:
            print(f"❌ Connection test failed: {exc}")
            return False

    # ------------------------------------------------------------------
    # Main flow
    # ------------------------------------------------------------------

    def setup_token_auth(self, refresh_token: bool = False) -> bool:
        """Run the full auth setup flow."""
        print("🚀 Databricks authentication setup")
        print(f"   Workspace: {self.workspace_root}")
        print(f"   Env file:  {self.env_file}")
        print()

        if not self._ensure_credentials_in_env():
            return False

        if refresh_token:
            print("🔄 Refreshing token via OAuth browser login...")
            if not self.run_oauth_login():
                return False

        token = self.extract_token()
        if not token:
            return False

        return self.update_env_file(token)


def main() -> int:
    parser = argparse.ArgumentParser(description="Databricks token authentication setup")
    parser.add_argument("--refresh-token", action="store_true", help="Force OAuth browser login")
    parser.add_argument("--test-connection", action="store_true", help="Test connection after setup")
    parser.add_argument("--workspace", type=Path, help="Workspace root (default: cwd)")
    args = parser.parse_args()

    setup = DatabricksTokenSetup(workspace_root=args.workspace)

    success = setup.setup_token_auth(refresh_token=args.refresh_token)

    if success and args.test_connection:
        setup.test_connection()

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
