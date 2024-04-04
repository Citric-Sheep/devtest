"""Command Line Interface"""

import click


@click.command()
@click.option(
    "--max-floors",
    default=10,
    help="Building floors quantity.",
    prompt="How many floors does the building have?",
)
@click.option(
    "--trips",
    default=100,
    prompt="How many trips?",
    help="Amount of trips to simulate.",
)
def hello(max_floors, trips):
    """Simple program."""
    click.echo(f"Trips per floor {int(trips/max_floors)}")


if __name__ == "__main__":
    hello()
