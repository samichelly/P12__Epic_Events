import click
from datetime import datetime, timedelta
from decimal import Decimal
from rich import print
from rich.console import Console
from rich.table import Table

from table import display_customers, display_contracts, display_events
from models import User, Customer, Contract, Event, session
from permissions import (
    read_permission,
    sales_permission,
    management_permission,
    support_permission,
)


class Context:
    def __init__(self):
        # self.user = None
        self.user = (
            session.query(User).filter_by(email="xav@laine.com", password="xavier").first()
        )
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
    user = session.query(User).filter_by(email=email).first()

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
        customers = session.query(Customer).all()
        display_customers(customers)

        if not customers:
            print("[bold yellow]No customers found.[/bold yellow]")
            return


@cli.command()
# @authenticated_users.command()
@pass_context
def list_contracts(ctx):
    """List all contracts."""
    if read_permission(ctx):
        contracts = session.query(Contract).all()
        display_contracts(contracts)

        if not contracts:
            print("[bold yellow]No customers found.[/bold yellow]")
            return


@cli.command()
# @authenticated_users.command()
@pass_context
def list_events(ctx):
    """List all events."""
    if read_permission(ctx):
        events = session.query(Event).all()
        display_events(events)

        if not events:
            print("[bold yellow]No events found.[/bold yellow]")
            return


@cli.command()
@pass_context
def create_customer(ctx):
    """Create a new customer."""
    if sales_permission(ctx):
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
        # print(ctx.customer)


@cli.command()
@pass_context
def update_customer(ctx):
    """Update a customer."""
    if sales_permission(ctx):
        customer_email = click.prompt("Enter Customer Email to update", type=str)
        customer = session.query(Customer).filter_by(email=customer_email).first()

        if customer:
            click.echo("Updating customer:")
            first_name = click.prompt(
                "Customer First Name", type=str, default=customer.first_name
            )
            last_name = click.prompt(
                "Customer Last Name", type=str, default=customer.last_name
            )
            email = click.prompt("Customer Email", type=str, default=customer.email)
            phone = click.prompt("Customer Phone", type=str, default=customer.phone)
            company_name = click.prompt(
                "Customer Company Name", type=str, default=customer.company_name
            )

            # Update customer fields
            customer.first_name = first_name
            customer.last_name = last_name
            customer.email = email
            customer.phone = phone
            customer.company_name = company_name

            session.commit()
            print("[bold green]Customer updated successfully[/bold green].")
            ctx.customer = customer
            print(ctx.customer)
        else:
            print(f"No customer found with email {customer_email}.")


@cli.command()
@pass_context
def create_contract(ctx):
    """Create a new contract."""
    if management_permission(ctx):
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
def update_contract(ctx):
    """Update a contract."""
    if management_permission(ctx):
        contract_id = click.prompt("Enter Contract ID to update", type=int)
        contract = session.get(Contract, contract_id)

        if contract:
            click.echo("Updating contract:")
            total_amount = click.prompt(
                "Total Amount", type=str, default=str(contract.total_amount)
            )
            remaining_amount = click.prompt(
                "Remaining Amount", type=str, default=str(contract.remaining_amount)
            )
            is_signed_input = click.prompt(
                "Is the contract signed? (y/n)",
                type=str,
                default="y" if contract.is_signed else "n",
            )
            is_signed = is_signed_input.lower() == "y"

            # Update contract fields
            contract.total_amount = total_amount
            contract.remaining_amount = remaining_amount
            contract.is_signed = is_signed

            session.commit()
            print("[bold green]Contract updated successfully[/bold green].")
        else:
            print(f"No contract found with ID {contract_id}.")


@cli.command()
@pass_context
def create_event(ctx):
    """Create a new event."""
    if sales_permission(ctx):
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
            support_contact_id=None,
        )

        session.add(new_event)
        session.commit()
        print("[bold green]Event created successfully[/bold green].")


@cli.command()
@pass_context
def update_event(ctx):
    """Assign support event."""
    user_role = ctx.user.role.name
    try:
        if user_role in ["support", "management"]:
            event_id = click.prompt("Enter Event ID to update", type=int)
            event = session.get(Event, event_id)

            if event and user_role == "support":
                click.echo(f"Updating event: {event.event_name}:")

                event_name = click.prompt(
                    "Event Name", default=event.event_name, type=str
                )
                event_date_start = click.prompt(
                    "Event Start Date (YYYY-MM-DD HH:MM)",
                    default=event.event_date_start,
                    type=click.DateTime(),
                )
                event_date_end = click.prompt(
                    "Event End Date (YYYY-MM-DD HH:MM)",
                    default=event.event_date_end,
                    type=click.DateTime(),
                )
                location = click.prompt(
                    "Event Location", default=event.location, type=str
                )
                attendees = click.prompt(
                    "Number of Attendees", default=event.attendees, type=int
                )
                notes = click.prompt("Event Notes", default=event.notes, type=str)

                event.event_name = event_name
                event.event_date_start = event_date_start
                event.event_date_end = event_date_end
                event.location = location
                event.attendees = attendees
                event.notes = notes
                session.commit()
                click.echo("[bold green]Event operation completed[/bold green].")

            elif event and user_role == "management":
                click.echo(f"Assign support event: {event.event_name}:")
                support_email = click.prompt("Enter Support Contact Email", type=str)
                support_user = (
                    session.query(User)
                    .filter_by(email=support_email, role="support")
                    .first()
                )

                if support_user:
                    event.support_contact_id = support_user.id
                    session.commit()
                    click.echo("[bold green]Event operation completed[/bold green].")
                else:
                    click.echo(
                        f"{support_email} is not a support user. Support contact not assigned."
                    )

            else:
                click.echo(f"Event with ID {event_id} not found.")
        else:
            click.echo("User does not have the required role for this operation.")

    except Exception as e:
        click.echo(f"Error : {e}")


if __name__ == "__main__":
    cli()
