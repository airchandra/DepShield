"""Configuration management for DepShield."""

from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class DepShieldConfig(BaseSettings):
    """Main configuration for DepShield."""

    # Repository input
    repos: list[str] = []
    output_dir: Path = Path("./depshield-output")

    # Execution mode
    dry_run: bool = True
    apply: bool = False
    verbose: bool = False

    # Ecosystem filtering
    ecosystems: list[str] = ["jvm", "python", "javascript", "go", "rust"]

    # Tool paths
    syft_path: str = "syft"
    grype_path: str = "grype"
    osv_scanner_path: str = "osv-scanner"
    trivy_path: str = "trivy"

    # OpenRewrite
    openrewrite_recipes_dir: Path = Path("./openrewrite-recipes")

    model_config = SettingsConfigDict(
        env_prefix="DEPSHIELD_",
        env_nested_delimiter="__"
    )
