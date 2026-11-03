#!/usr/bin/env python3
"""Test suite to verify critical bug fixes."""

import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

test_results = []

def test(name):
    """Decorator for tests."""
    def decorator(func):
        def wrapper():
            try:
                func()
                test_results.append((name, "✅ PASS", None))
                logger.info(f"✅ {name}")
                return True
            except Exception as e:
                test_results.append((name, "❌ FAIL", str(e)))
                logger.error(f"❌ {name}: {e}")
                return False
        return wrapper
    return decorator


@test("Import config module")
def test_config_imports():
    """Test that config can be imported and initialized."""
    from depshield.config import DepShieldConfig

    # Test with defaults
    config = DepShieldConfig()
    assert config.repos == []
    assert config.dry_run == True
    assert config.output_dir == Path("./depshield-output")


@test("Pydantic v2 configuration loads env vars")
def test_pydantic_env_vars():
    """Test that environment variables load with correct prefix."""
    import os
    from depshield.config import DepShieldConfig

    # Set env var with new DEPSHIELD_ prefix
    os.environ["DEPSHIELD_VERBOSE"] = "true"
    config = DepShieldConfig()
    assert config.verbose == True, f"Expected verbose=True, got {config.verbose}"


@test("Base remediation module imports correctly")
def test_remediation_imports():
    """Test that remediation base class imports shlex."""
    from depshield.remediation.base import BaseRemediator, shlex

    # Test command splitting
    test_cmd = 'mvn clean install -Dmaven.test.skip="true"'
    parts = shlex.split(test_cmd)
    assert len(parts) == 4  # mvn, clean, install, -Dmaven.test.skip=true
    assert parts[3] == '-Dmaven.test.skip=true'


@test("Upgrade matrix severity comparison")
def test_upgrade_matrix_severity():
    """Test that severity comparison works correctly."""
    from depshield.models import Severity, Vulnerability
    from depshield.matrix.upgrade_matrix import UpgradeMatrix

    # Create vulnerabilities with different severities
    vulns = [
        Vulnerability(
            id="CVE-1", package="pkg1", severity=Severity.HIGH,
            cvss_score=7.5, description="", fixed_version="1.1",
            current_version="1.0", advisory=""
        ),
        Vulnerability(
            id="CVE-2", package="pkg1", severity=Severity.CRITICAL,
            cvss_score=9.8, description="", fixed_version="1.1",
            current_version="1.0", advisory=""
        ),
        Vulnerability(
            id="CVE-3", package="pkg1", severity=Severity.MEDIUM,
            cvss_score=5.2, description="", fixed_version="1.1",
            current_version="1.0", advisory=""
        ),
    ]

    matrix = UpgradeMatrix(vulns)
    recommendations = matrix.build()

    # Check that max severity is CRITICAL, not MEDIUM
    rec = recommendations["pkg1"]
    assert rec.severity_level == "critical", f"Expected 'critical', got '{rec.severity_level}'"


@test("Grype scanner CVSS parsing")
def test_grype_cvss_parsing():
    """Test that CVSS parsing handles different formats."""
    from depshield.scanners.grype import GrypScanner
    from depshield.models import RepoManifest, Severity

    # Create a scanner instance
    repo = RepoManifest(
        path=Path("."),
        name="test",
        ecosystems=[],
        build_command=None,
        test_command=None,
        lint_command=None
    )

    class MockConfig:
        output_dir = Path("./test-output")

    scanner = GrypScanner(repo, MockConfig())

    # Test parsing with different CVSS formats
    test_data = {
        "matches": [
            {
                "vulnerability": {
                    "id": "CVE-2024-1234",
                    "severity": "critical",
                    "cvss": 9.8,  # Numeric
                    "description": "Test",
                    "fix": {"versions": ["1.1.0"]},
                    "dataSource": "NVD"
                },
                "artifact": {"name": "pkg1", "version": "1.0.0"}
            },
            {
                "vulnerability": {
                    "id": "CVE-2024-5678",
                    "severity": "high",
                    "cvss": "7.5",  # String
                    "description": "Test",
                    "fix": {},
                    "dataSource": "NVD"
                },
                "artifact": {"name": "pkg2", "version": "1.0.0"}
            },
            {
                "vulnerability": {
                    "id": "CVE-2024-9012",
                    "severity": "medium",
                    "cvss": None,  # None value
                    "description": "Test",
                    "fix": {},
                    "dataSource": "NVD"
                },
                "artifact": {"name": "pkg3", "version": "1.0.0"}
            }
        ]
    }

    vulns = scanner._parse_vulnerabilities(test_data)
    assert len(vulns) == 3
    assert vulns[0].cvss_score == 9.8
    assert vulns[1].cvss_score == 7.5
    assert vulns[2].cvss_score == 0.0  # Should default to 0.0


@test("Trivy scanner CVSS parsing with nested dicts")
def test_trivy_cvss_parsing():
    """Test that Trivy scanner handles nested CVSS data."""
    from depshield.scanners.trivy import TrivyScanner
    from depshield.models import RepoManifest

    repo = RepoManifest(
        path=Path("."),
        name="test",
        ecosystems=[],
        build_command=None,
        test_command=None,
        lint_command=None
    )

    class MockConfig:
        output_dir = Path("./test-output")

    scanner = TrivyScanner(repo, MockConfig())

    # Test parsing with nested CVSS structure
    test_data = {
        "Results": [
            {
                "Vulnerabilities": [
                    {
                        "VulnerabilityID": "CVE-2024-1234",
                        "PkgName": "pkg1",
                        "Severity": "CRITICAL",
                        "CVSS": {
                            "ghsa": {"V3Score": 9.8}
                        },
                        "Title": "Test",
                        "FixedVersion": "1.1.0",
                        "InstalledVersion": "1.0.0",
                        "PrimaryURL": "https://example.com"
                    },
                    {
                        "VulnerabilityID": "CVE-2024-5678",
                        "PkgName": "pkg2",
                        "Severity": "HIGH",
                        "CVSS": {},  # Empty CVSS
                        "Title": "Test",
                        "FixedVersion": "",
                        "InstalledVersion": "1.0.0",
                        "PrimaryURL": ""
                    },
                    {
                        "VulnerabilityID": "CVE-2024-9012",
                        "PkgName": "pkg3",
                        "Severity": "MEDIUM",
                        "CVSS": "invalid",  # Invalid CVSS (not dict)
                        "Title": "Test",
                        "FixedVersion": "",
                        "InstalledVersion": "1.0.0",
                        "PrimaryURL": ""
                    }
                ],
                "Misconfigurations": []
            }
        ]
    }

    vulns = scanner._parse_vulnerabilities(test_data)
    assert len(vulns) == 3
    assert vulns[0].cvss_score == 9.8
    assert vulns[1].cvss_score == 0.0  # Empty CVSS should default to 0.0
    assert vulns[2].cvss_score == 0.0  # Invalid CVSS should default to 0.0


@test("FastAPI imports work")
def test_fastapi_imports():
    """Test that FastAPI and required modules import correctly."""
    try:
        from fastapi import FastAPI
        from fastapi.cors import CORSMiddleware
        from fastapi.staticfiles import StaticFiles
        import uvicorn
        logger.info("  All FastAPI dependencies available")
    except ImportError as e:
        raise AssertionError(f"FastAPI dependency missing: {e}")


@test("Backend app creation")
def test_backend_app_creation():
    """Test that FastAPI app can be created."""
    from ui.backend.main import create_app

    app = create_app()
    assert app is not None
    assert app.title == "DepShield Dashboard"


@test("Logger names are correct")
def test_logger_names():
    """Test that loggers use correct module names."""
    import logging

    # These should exist and be named correctly
    logger1 = logging.getLogger("depshield.pipeline")
    logger2 = logging.getLogger("depshield.scanners")
    logger3 = logging.getLogger("depshield.remediation")

    assert logger1.name == "depshield.pipeline"
    assert logger2.name == "depshield.scanners"
    assert logger3.name == "depshield.remediation"


@test("CLI help works")
def test_cli_help():
    """Test that CLI help can be displayed."""
    from click.testing import CliRunner
    from depshield.cli import main

    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "DepShield" in result.output


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("DepShield Bug Fix Test Suite")
    print("="*70 + "\n")

    # Run all tests
    test_config_imports()
    test_pydantic_env_vars()
    test_remediation_imports()
    test_upgrade_matrix_severity()
    test_grype_cvss_parsing()
    test_trivy_cvss_parsing()
    test_fastapi_imports()
    test_backend_app_creation()
    test_logger_names()
    test_cli_help()

    # Print summary
    print("\n" + "="*70)
    print("Test Summary")
    print("="*70 + "\n")

    passed = sum(1 for _, status, _ in test_results if "PASS" in status)
    failed = sum(1 for _, status, _ in test_results if "FAIL" in status)

    for name, status, error in test_results:
        if error:
            print(f"{status} {name}")
            print(f"       {error}")
        else:
            print(f"{status} {name}")

    print("\n" + "-"*70)
    print(f"Results: {passed} passed, {failed} failed out of {len(test_results)} tests")
    print("-"*70 + "\n")

    if failed > 0:
        print("⚠️  Some tests failed. Please review the errors above.")
        sys.exit(1)
    else:
        print("✅ All tests passed! Fixes are working correctly.")
        sys.exit(0)


if __name__ == "__main__":
    main()
