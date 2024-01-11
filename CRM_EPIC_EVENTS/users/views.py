import click
from datetime import datetime, timedelta
from decimal import Decimal
from rich import print
from rich.console import Console
from rich.table import Table


from models import User, Customer, Contract, Event, session
from permissions import (
    read_permission,
    create_customer_permission,
    create_event_permission,
    create_contract_permission,
    update_event_permission,
)


class Context:
    def __init__(self):
        self.user = None
        # self.user = (
        #     session.query(User)
        #     .filter_by(email="xav@laine.com", password="xavier")
        #     .first()
        # )
        self.customer = None


pass_context = click.make_pass_decorator(Context, ensure=True)


@click.group()
@click.pass_context
def cli(context):
    """CRM Epic Events"""
    context.obj = Context()


@cli.command()
@pass_context
def print_context(context):
    """Authenticate a user."""
    print(context.user)
    # print(context.user.email)

@cli.command()
@pass_context
def login(context):
    """Authenticate a user."""
    email = click.prompt("Email", type=str)
    password = click.prompt("Password", type=str, hide_input=True)
    # user = session.query(User).filter_by(email=email, password=password).first()
    
    user = session.query(User).filter_by(email=email).first()

    print("user : ", user)
    print("return hash :", user.check_password(password))

    if user and user.check_password(password):
        print(
            f"[bold green]Authentication successful[/bold green] for user with email {user.email}"
        )
        context.user = user
        print("context")
        print(context.user.email)
    else:
        print("Authentication failed.")


@cli.command()
@pass_context
def input_new_user(ctx):
    """Create a new user."""
    click.echo("Creating a new user:")
    email = click.prompt("Email", type=str)
    password = click.prompt(
        "Password", type=str, hide_input=True, confirmation_prompt=True
    )
    first_name = click.prompt("First Name", type=str)
    last_name = click.prompt("Last Name", type=str)
    role = click.prompt("Role", type=click.Choice(["sales", "support", "management"]))

    new_user = User(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        role=role,
    )
    session.add(new_user)
    session.commit()
    print("[bold green]User created successfully[/bold green].")


# def create_authenticated_users_cli():
#     @click.group()
#     @pass_context
#     def authenticated_users(context):
#         """Commands for authenticated users"""
#         print("OKKKKKKK")
#         print(context)
#         # context.obj = Context()

#     @authenticated_users.command()
#     def list_events():
#         """List all events."""
#         print("dans la nouvelle commande")


# @cli.group()
# @click.pass_context
@click.group()
@pass_context
def authenticated_users(context):
    """Commands for authenticated users"""
    print("OKKKKKKK")
    print(context)
    # context.obj = Context()


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


@cli.command()
@pass_context
def list_customers(ctx):
    """List all customers."""
    if read_permission(ctx):
        # print(ctx.user)
        # print(ctx.user.role)
        console = Console()
        customers = session.query(Customer).all()

        if not customers:
            print("[bold yellow]No customers found.[/bold yellow]")
            return

        # print("[bold cyan]List of customers:[/bold cyan]")
        table = Table(title="List of customers")
        table.add_column("Full Name", style="cyan")
        table.add_column("Email", style="magenta")
        table.add_column("Phone", style="cyan")
        table.add_column("Company Name", style="magenta")
        table.add_column("Date Registred", style="cyan")
        table.add_column("Last Contact", style="magenta")
        

        for customer in customers:
            table.add_row(
                customer.__repr__(),
                customer.email,
                customer.phone,
                customer.company_name,
                format_value(customer.creation_date),
                format_value(customer.last_contact_date)
            )
            # table.add_row(customer.id, customer, customer.email)

            # print(f"[cyan]{customer.id} - {customer} - {customer.email}[/cyan]")
    # console = Console()
    console.print(table)


@cli.command()
# @authenticated_users.command()
@pass_context
def list_contracts(ctx):
    """List all contracts."""
    if read_permission(ctx):
        console = Console()
        contracts = session.query(Contract).all()

        if not contracts:
            print("[bold yellow]No contracts found.[/bold yellow]")
            return

        table = Table(title="List of contracts")
        table.add_column("Total Amount", style="cyan")
        table.add_column("Remaining Amount", style="magenta")
        table.add_column("Creation Date", style="cyan")
        table.add_column("Signed", style="magenta")
        for contract in contracts:
            table.add_row(
                format_value(contract.total_amount),
                format_value(contract.remaining_amount),
                format_value(contract.creation_date),
                format_value(contract.is_signed),
            )

    console.print(table)


@cli.command()
# @authenticated_users.command()
@pass_context
def list_events(ctx):
    """List all events."""
    if read_permission(ctx):
        console = Console()
        events = session.query(Event).all()

        if not events:
            print("[bold yellow]No events found.[/bold yellow]")
            return

        print("[bold cyan]List of events:[/bold cyan]")
        table = Table(title="List of events")
        table.add_column("Event Name", style="cyan")
        table.add_column("Date Start", style="magenta")
        table.add_column("Date End", style="cyan")
        table.add_column("Location", style="magenta")
        table.add_column("Attendees", style="cyan")
        table.add_column("Notes", style="magenta")
        for event in events:
            # print(
            #     f"[cyan]{event.event_name} - {event.event_date_start} - {event.event_date_end}[/cyan]"
            # )

            table.add_row(
                event.event_name,
                format_value(event.event_date_start),
                format_value(event.event_date_end),
                event.location,
                format_value(event.attendees),
                format_value(event.notes),
            )

    console.print(table)


@cli.command()
@pass_context
def create_new_customer(ctx):
    """Create a new customer."""
    if create_customer_permission(ctx):
        # new_user = (
        #     session.query(User).filter_by(email="jh@support.com", password="aqa").first()
        # )
        print("ctx.user.id : ", ctx.user.id)
        click.echo("Creating a new customer:")
        first_name = click.prompt("Customer First Name", type=str)
        last_name = click.prompt("Customer Last Name", type=str)
        email = click.prompt("Customer Email", type=str)
        phone = click.prompt("Customer Phone", type=str)
        company_name = click.prompt("Customer Company Name", type=str)

        new_customer = Customer(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            company_name=company_name,
            sales_contact_id=ctx.user.id,
        )

        session.add(new_customer)
        session.commit()
        print("[bold green]Customer created successfully[/bold green].")
        ctx.customer = new_customer
        print(ctx.customer)
        # context = click.get_current_context()
        # print("okkkkk")
        # context.invoke(create_new_contract)


@cli.command()
@pass_context
def create_new_contract(ctx):
    """Create a new contract."""
    if create_contract_permission(ctx):
        print("dans la seconde commande")

        # user = session.query(User).filter_by(email="jh@support.com", password="aqa").first()
        customer = session.query(Customer).first()

        print("customer : ", customer)

        click.echo("Creating a new contract:")
        total_amount = click.prompt("Total Amount", type=str)
        remaining_amount = click.prompt("Remaining Amount", type=str)
        is_signed_input = click.prompt("Is the contract signed? (y/n)", type=str)
        is_signed = is_signed_input.lower() == "y"

        new_contract = Contract(
            total_amount=total_amount,
            remaining_amount=remaining_amount,
            is_signed=is_signed,
            customer_id=customer.id,
            management_contact_id=ctx.user.id,
        )

        session.add(new_contract)
        session.commit()
        print("[bold green]Contract created successfully[/bold green].")


@cli.command()
@pass_context
def create_new_event(ctx):
    """Create a new event."""
    if create_event_permission(ctx):
        # user = session.query(User).filter_by(email="guy@toul.com", password="asa").first()
        contract = session.query(Contract).first()

        click.echo("Creating a new event:")

        event_name = click.prompt("Event Name", type=str)

        event_date_start = click.prompt(
            "Event Start Date (YYYY-MM-DD HH:MM)", type=click.DateTime()
        )
        event_date_end = click.prompt(
            "Event End Date (YYYY-MM-DD HH:MM)", type=click.DateTime()
        )

        location = click.prompt("Event Location", type=str)
        attendees = click.prompt("Number of Attendees", type=int)
        notes = click.prompt("Event Notes", type=str)

        new_event = Event(
            event_name=event_name,
            event_date_start=event_date_start,
            event_date_end=event_date_end,
            location=location,
            attendees=attendees,
            notes=notes,
            contract_id=contract.id,
            support_contact_id=ctx.user.id,
        )

        session.add(new_event)
        session.commit()
        print("[bold green]Event created successfully[/bold green].")


if __name__ == "__main__":
    cli()
    # valid_login = cli()
    # print(valid_login)
    # authenticated_users()
