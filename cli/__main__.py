"""Command Line Interface"""

import click

from core.service import run_simulation


@click.command("run")
@click.option(
    "--max-floor",
    default=10,
    help="Building floors quantity.",
    prompt="Top Floor",
)
@click.option(
    "--trips",
    default=100,
    prompt="How many trips?",
    help="Trips Qty.",
)
def run(max_floor: int, trips: int):
    """Run the simulation."""
    click.echo("Starting simulation.")
    run_simulation(top_floor=max_floor, sample_size=trips)


@click.group()
def main():
    """Elevator Simulator CLI"""
    click.echo("Welcome to Elevator Simulator!")


main.add_command(run)


if __name__ == "__main__":
    main()
