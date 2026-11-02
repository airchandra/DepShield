"""Tests for report generation."""

import pytest

from depshield.models import Dependency, Ecosystem, RepoManifest, Severity, Vulnerability
from depshield.reporters.architecture import ArchitectureReporter
from depshield.reporters.diagrams import DiagramGenerator
from depshield.reporters.sbom_report import SBOMReporter
from depshield.reporters.vuln_report import VulnerabilityReporter


def test_sbom_reporter_empty():
    """Test SBOM report with no dependencies."""
    report = SBOMReporter.format_sbom([])
    assert "No dependencies found" in report


def test_sbom_reporter_with_deps():
    """Test SBOM report with dependencies."""
    deps = [
        Dependency(name="requests", version="2.28.0", ecosystem=Ecosystem.PYTHON, license="Apache-2.0"),
        Dependency(name="numpy", version="1.23.0", ecosystem=Ecosystem.PYTHON, license="BSD"),
    ]

    report = SBOMReporter.format_sbom(deps)
    assert "requests" in report
    assert "numpy" in report
    assert "Apache-2.0" in report


def test_vulnerability_reporter_empty():
    """Test vulnerability report with no vulns."""
    report = VulnerabilityReporter.format_vulnerabilities([])
    assert "No vulnerabilities found" in report


def test_vulnerability_reporter_with_vulns():
    """Test vulnerability report with vulnerabilities."""
    vulns = [
        Vulnerability(
            id="CVE-2022-1234",
            package="log4j",
            severity=Severity.CRITICAL,
            cvss_score=9.8,
            description="Critical RCE vulnerability",
            fixed_version="2.17.1"
        ),
        Vulnerability(
            id="CVE-2022-5678",
            package="requests",
            severity=Severity.HIGH,
            cvss_score=7.5,
            description="Medium-severity issue",
            fixed_version="2.28.0"
        ),
    ]

    report = VulnerabilityReporter.format_vulnerabilities(vulns)
    assert "CVE-2022-1234" in report
    assert "log4j" in report
    assert "CRITICAL" in report


def test_vulnerability_reporter_sorted_by_severity():
    """Test that vulnerabilities are sorted by severity."""
    vulns = [
        Vulnerability(
            id="CVE-1",
            package="pkg-low",
            severity=Severity.LOW,
            fixed_version="1.0"
        ),
        Vulnerability(
            id="CVE-2",
            package="pkg-critical",
            severity=Severity.CRITICAL,
            fixed_version="1.0"
        ),
    ]

    report = VulnerabilityReporter.format_vulnerabilities(vulns)
    # Critical should appear before Low in the report
    critical_pos = report.find("pkg-critical")
    low_pos = report.find("pkg-low")
    assert critical_pos < low_pos


def test_architecture_reporter_system():
    """Test system architecture report."""
    repos = [
        RepoManifest(
            path="/repo1",
            name="repo1",
            ecosystems=[Ecosystem.JVM],
            build_command="mvn clean package"
        ),
        RepoManifest(
            path="/repo2",
            name="repo2",
            ecosystems=[Ecosystem.PYTHON],
            build_command="python setup.py build"
        ),
    ]

    report = ArchitectureReporter.format_system_architecture(repos)
    assert "repo1" in report
    assert "repo2" in report
    assert "JVM" in report or "jvm" in report


def test_diagram_generator_c4_context():
    """Test C4 context diagram generation."""
    repos = [
        RepoManifest(path="/repo1", name="Service A", ecosystems=[Ecosystem.JVM]),
        RepoManifest(path="/repo2", name="Service B", ecosystems=[Ecosystem.PYTHON]),
    ]

    diagram = DiagramGenerator.c4_context_diagram(repos, "My System")
    assert "mermaid" in diagram
    assert "Service A" in diagram
    assert "Service B" in diagram


def test_diagram_generator_sequence():
    """Test sequence diagram generation."""
    phases = ["Discovery", "SBOM", "Scanning"]
    diagram = DiagramGenerator.pipeline_sequence_diagram(phases)
    assert "mermaid" in diagram
    assert "sequenceDiagram" in diagram


def test_diagram_generator_flowchart():
    """Test remediation flowchart generation."""
    diagram = DiagramGenerator.remediation_flowchart()
    assert "mermaid" in diagram
    assert "flowchart" in diagram
    assert "Build" in diagram
