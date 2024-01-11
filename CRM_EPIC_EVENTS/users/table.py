from rich.console import Console
from rich.table import Table
from rich.theme import Theme
from rich.text import Text

from datetime import datetime
from decimal import Decimal


def format_value(value):
    """Format a value for display in a table."""
    if isinstance(value, Decimal):
        return f"{value:.2f}"
    elif isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(value, bool):
        return "Yes" if value else "No"
    else:
        return str(value)


def display_customers(customers):
    console = Console()

    if not customers:
        console.print("[bold yellow]No customers found.[/bold yellow]")
        return

    table = Table(
        title="List of customers",
        show_header=True,
        header_style="bold yellow",
        padding=(0, 2),
    )

    table.add_column("Full Name", style="cyan")
    # table.add_column("Email", style="magenta")
    # table.add_column("Phone", style="cyan")
    table.add_column("Company Name", style="magenta")
    table.add_column("Date Registered", style="cyan")
    table.add_column("Last Contact", style="magenta")

    for customer in customers:
        table.add_row(
            customer.__repr__(),
            # customer.email,
            # customer.phone,
            customer.company_name,
            format_value(customer.creation_date),
            format_value(customer.last_contact_date),
        )

    console.print(table)


def display_contracts(contracts):
    console = Console()

    if not contracts:
        console.print("[bold yellow]No contracts found.[/bold yellow]")
        return

    table = Table(
        title="List of contracts",
        show_header=True,
        header_style="bold yellow",
        padding=(0, 2),
    )

    table.add_column("ID", style="magenta")
    table.add_column("Total Amount", style="cyan")
    table.add_column("Remaining Amount", style="magenta")
    table.add_column("Creation Date", style="cyan")
    table.add_column("Signed", style="magenta")

    for contract in contracts:
        table.add_row(
            format_value(contract.id),
            format_value(contract.total_amount),
            format_value(contract.remaining_amount),
            format_value(contract.creation_date),
            format_value(contract.is_signed),
        )

    console.print(table)


def display_events(events):
    console = Console()

    if not events:
        console.print("[bold yellow]No events found.[/bold yellow]")
        return

    table = Table(
        title="List of events",
        show_header=True,
        header_style="bold yellow",
        padding=(0, 2),
    )

    table.add_column("Event Name", style="cyan")
    table.add_column("Date Start", style="magenta")
    table.add_column("Date End", style="cyan")
    table.add_column("Location", style="magenta")
    table.add_column("Attendees", style="cyan")
    table.add_column("Notes", style="magenta")

    for event in events:
        table.add_row(
            event.event_name,
            format_value(event.event_date_start),
            format_value(event.event_date_end),
            event.location,
            format_value(event.attendees),
            format_value(event.notes),
        )

    console.print(table)
