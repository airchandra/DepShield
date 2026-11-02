"""Command-line interface for DepShield."""

import logging
from pathlib import Path

import click

from depshield.config import DepShieldConfig
from depshield.pipeline import DepShieldPipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "--repos",
    "-r",
    multiple=True,
    required=True,
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Path(s) to git repositories to scan"
)
@click.option(
    "--output",
    "-o",
    type=click.Path(file_okay=False, dir_okay=True),
    default="./depshield-output",
    help="Output directory for reports"
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=True,
    help="Generate reports without applying changes (default: True)"
)
@click.option(
    "--apply",
    is_flag=True,
    default=False,
    help="Apply remediation changes (requires --dry-run to be False)"
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    default=False,
    help="Enable verbose logging"
)
@click.option(
    "--ecosystems",
    "-e",
    multiple=True,
    type=click.Choice(["jvm", "python", "javascript", "go", "rust"]),
    help="Limit scanning to specific ecosystems"
)
def main(repos, output, dry_run, apply, verbose, ecosystems):
    """DepShield — Zero-critical-vulnerabilities pipeline.

    Scan one or more git repositories for vulnerabilities across a distributed
    system, remediate dependencies to stable versions, and generate comprehensive
    documentation including SBOM, vulnerability reports, architecture diagrams,
    and upgrade matrices.
    """
    # Adjust logging level
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Validate options
    if apply and dry_run:
        click.secho(
            "⚠️  --apply requires --dry-run=False. Use: depshield ... --no-dry-run --apply",
            fg="yellow"
        )
        raise click.Exit(1)

    # Build configuration
    config = DepShieldConfig(
        repos=list(repos),
        output_dir=Path(output),
        dry_run=dry_run,
        apply=apply,
        verbose=verbose,
        ecosystems=list(ecosystems) if ecosystems else ["jvm", "python", "javascript", "go", "rust"]
    )

    # Display configuration
    click.secho("🚀 DepShield", fg="cyan", bold=True)
    click.echo(f"Repositories: {', '.join(config.repos)}")
    click.echo(f"Output: {config.output_dir}")
    click.echo(f"Mode: {'DRY RUN' if config.dry_run else 'APPLY'}")
    click.echo(f"Ecosystems: {', '.join(config.ecosystems)}")
    click.echo("")

    # Run pipeline
    try:
        pipeline = DepShieldPipeline(config)
        pipeline.run()

        click.secho("✅ Pipeline completed successfully", fg="green", bold=True)
        click.echo(f"Reports available at: {config.output_dir}")

    except Exception as e:
        click.secho(f"❌ Pipeline failed: {e}", fg="red", bold=True)
        if verbose:
            logger.exception("Exception details:")
        raise click.Exit(1)


if __name__ == "__main__":
    main()
