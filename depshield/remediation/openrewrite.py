"""JVM remediation using OpenRewrite."""

import logging
import xml.etree.ElementTree as ET
from pathlib import Path

from depshield.models import RemediationResult, RepoManifest
from depshield.remediation.base import BaseRemediator

logger = logging.getLogger(__name__)


class OpenRewriteRemediator(BaseRemediator):
    """Remediate JVM projects using OpenRewrite."""

    def remediate(self, dry_run: bool = True) -> RemediationResult:
        """Apply OpenRewrite recipes to remediate dependencies.

        Args:
            dry_run: If True, only report without applying changes

        Returns:
            RemediationResult with upgrade summary
        """
        try:
            # Detect build tool (Maven or Gradle)
            pom_path = self.repo.path / "pom.xml"
            gradle_path = self.repo.path / "build.gradle"

            if not pom_path.exists() and not gradle_path.exists():
                self.result.error = "No pom.xml or build.gradle found"
                return self.result

            if pom_path.exists():
                return self._remediate_maven(dry_run)
            else:
                return self._remediate_gradle(dry_run)

        except Exception as e:
            self.result.error = f"OpenRewrite remediation error: {str(e)}"
            logger.error(f"Exception in OpenRewrite remediation: {e}")
            return self.result

    def _remediate_maven(self, dry_run: bool) -> RemediationResult:
        """Remediate Maven projects."""
        try:
            if not dry_run:
                self._create_stash()

            # Run OpenRewrite Maven plugin
            cmd = [
                "mvn", "openrewrite:run",
                "-DrecipeArtifactCoordinates=org.openrewrite:rewrite-all:latest",
                "-Drewrite.activeRecipes=org.openrewrite.java.dependencies.UpgradeDependencyVersion"
            ]

            stdout, stderr, rc = self._run_command(cmd, check=False)

            if rc != 0:
                if not dry_run:
                    self._pop_stash()
                self.result.error = f"Maven OpenRewrite failed: {stderr}"
                logger.error(f"Maven OpenRewrite failed: {stderr}")
                return self.result

            if not dry_run:
                build_ok, test_ok = self._build_and_test()
                self.result.build_succeeded = build_ok
                self.result.test_succeeded = test_ok

                if not build_ok or not test_ok:
                    self._pop_stash()
                    self.result.error = f"Build: {build_ok}, Tests: {test_ok}"
                    return self.result

            self.result.recipes_applied.append("org.openrewrite.java.dependencies.UpgradeDependencyVersion")
            self.result.success = True
            logger.info("Maven OpenRewrite remediation succeeded")

            return self.result

        except Exception as e:
            self.result.error = f"Maven remediation error: {str(e)}"
            logger.error(f"Exception in Maven remediation: {e}")
            return self.result

    def _remediate_gradle(self, dry_run: bool) -> RemediationResult:
        """Remediate Gradle projects."""
        try:
            if not dry_run:
                self._create_stash()

            # Run OpenRewrite Gradle plugin (assumes plugin is already in build.gradle)
            cmd = ["./gradlew", "rewriteRun"]

            stdout, stderr, rc = self._run_command(cmd, check=False)

            if rc != 0:
                if not dry_run:
                    self._pop_stash()
                self.result.error = f"Gradle OpenRewrite failed: {stderr}"
                logger.error(f"Gradle OpenRewrite failed: {stderr}")
                return self.result

            if not dry_run:
                build_ok, test_ok = self._build_and_test()
                self.result.build_succeeded = build_ok
                self.result.test_succeeded = test_ok

                if not build_ok or not test_ok:
                    self._pop_stash()
                    self.result.error = f"Build: {build_ok}, Tests: {test_ok}"
                    return self.result

            self.result.recipes_applied.append("org.openrewrite.java.dependencies.UpgradeDependencyVersion")
            self.result.success = True
            logger.info("Gradle OpenRewrite remediation succeeded")

            return self.result

        except Exception as e:
            self.result.error = f"Gradle remediation error: {str(e)}"
            logger.error(f"Exception in Gradle remediation: {e}")
            return self.result
