import click
import os
from datetime import datetime
from rich import print
from rich.padding import Padding
import sentry_sdk
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
        self.user = None


pass_context = click.make_pass_decorator(Context, ensure=True)


@click.group()
@click.pass_context
def cli(context):
    """CRM Epic Events"""
    context.obj = Context()


@cli.command()
@click.pass_context
def main(ctx):
    """Main command to choose between create_user and login."""
    in_app = True
    while in_app:
        choices = [
            "login",
            "exit",
        ]
        action = click.prompt("Select a choice", type=click.Choice(choices))

        if action == "login":
            log_in = ctx.invoke(login)
            if log_in is True:
                ctx.invoke(authenticated_users)
        elif action == "exit":
            in_app = False
            break
        else:
            pass


@cli.command()
@click.pass_context
def authenticated_users(ctx):
    """Main command to choose between various actions."""
    while True:
        key = click.prompt("Press a key + enter to load data")
        if key:
            ctx.invoke(lists_customers_contracts_events)

            choices = [
                "create_user",
                "create-customer",
                "create-contract",
                "create-event",
                "update-customer",
                "update-contract",
                "update-event",
                "delete-customer",
                "delete-contract",
                "delete-event",
                "delete-user",
                "logout",
            ]

            action = click.prompt("Select a choice", type=click.Choice(choices))

            if action == "create_user":
                ctx.invoke(create_user)
            elif action == "create-customer":
                ctx.invoke(create_customer)
            elif action == "create-contract":
                customer_id = click.prompt("Select ID Customer", type=int)
                ctx.forward(create_contract, customer_id)
            elif action == "create-event":
                contract_id = click.prompt("Select ID Contract", type=int)
                ctx.forward(create_event, contract_id)
            elif action == "update-customer":
                customer_id = click.prompt("Enter Customer ID to update", type=int)
                ctx.forward(update_customer, customer_id)
            elif action == "update-contract":
                contract_id = click.prompt("Enter Contract ID to update", type=int)
                ctx.forward(update_contract, contract_id)
            elif action == "update-event":
                event_id = click.prompt("Enter Event ID to update", type=int)
                ctx.forward(update_event, event_id)
            elif action == "delete-customer":
                customer_id = click.prompt("Enter Customer ID to delete", type=int)
                ctx.forward(delete_customer, customer_id)
            elif action == "delete-contract":
                contract_id = click.prompt("Enter Contract ID to delete", type=int)
                ctx.forward(delete_contract, contract_id)
            elif action == "delete-event":
                event_id = click.prompt("Enter Event ID to delete", type=int)
                ctx.forward(delete_event, event_id)
            elif action == "delete-user":
                deleted = ctx.invoke(delete_user)
                if deleted is True:
                    ctx.invoke(logout)
                    break
            elif action == "logout":
                ctx.invoke(logout)
                break
            else:
                pass


@cli.command()
@pass_context
def login(ctx):
    """Authenticate a user."""
    email = click.prompt("Email", type=str)
    password = click.prompt("Password", type=str, hide_input=True)
    user = session.query(User).filter_by(email=email).first()

    if user and user.check_password(password):
        print("[bold blue]Login...[/bold blue]")
        ctx.user = user
        print(
            f"[bold green]Authentication successful for user with email {user.email} [/bold green]"
        )
        return True
    else:
        print("[bold red]Authentication failed.[/bold red]")


@cli.command()
@pass_context
def logout(ctx):
    """Logout a user."""
    ctx.user = None
    print("[bold blue]Logout...[/bold blue]")


@cli.command()
@pass_context
def create_user(ctx):
    """Create a new user."""
    if management_permission(ctx):
        click.echo("Creating a new user:")
        email = click.prompt("Email", type=str)
        password = click.prompt(
            "Password", type=str, hide_input=True, confirmation_prompt=True
        )
        first_name = click.prompt("First Name", type=str)
        last_name = click.prompt("Last Name", type=str)
        phone_number = click.prompt("Phone Number", type=str)
        role = click.prompt(
            "Role", type=click.Choice(["sales", "support", "management"])
        )

        new_user = User(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            role=role,
        )

        try:
            session.add(new_user)
            session.commit()
            sentry_sdk.capture_message(f"User {new_user} created successfully!")
            print("[bold green]User created successfully[/bold green].")

        except Exception as e:
            print(f"[bold red]Error creating user: {e}[/bold red].")
            sentry_sdk.capture_message(f"Error creating user: {e}")


@cli.command()
@pass_context
def delete_user(ctx):
    """Delete user."""
    if management_permission(ctx):
        user_email = click.prompt("Enter User email to delete", type=str)
        user_to_delete = session.query(User).filter_by(email=user_email).first()

        if user_to_delete:
            role_name = user_to_delete.role.name
            user_to_delete.is_active = False
            user_to_delete.phone_number = None

            replacement_user = (
                session.query(User)
                .filter(
                    User.id != user_to_delete.id, User.role == role_name, User.is_active
                )
                .first()
            )

            if replacement_user:
                for customer in user_to_delete.customer_sales:
                    customer.sales_contact_id = replacement_user.id
                    print(
                        f"[bold yellow]{customer} reassigned to {replacement_user}[/bold yellow]."
                    )

                for contract in user_to_delete.contract_management:
                    contract.management_contact_id = replacement_user.id
                    print(
                        f"[bold yellow]Contract {contract.id} reassigned to {replacement_user}[/bold yellow]."
                    )

                for event in user_to_delete.event_support:
                    event.support_contact_id = replacement_user.id
                    print(
                        f"[bold yellow]{event.event_name} reassigned to {replacement_user}[/bold yellow]."
                    )

                session.commit()

                print("[bold green]User deleted successfully[/bold green].")
                return True
            else:
                print(
                    "[bold red]No remplacement user. Please create a new user with same role[/bold red]."
                )
        else:
            print("[bold red]No user to delete found[/bold red].")


@cli.command()
@pass_context
def lists_customers_contracts_events(ctx):
    """List all customers, contracts, events."""
    if read_permission(ctx):
        print(
            Padding(
                "[bold blue]Load Customers, Contracts and Events...[/bold blue]", (1, 0)
            )
        )
        customers = session.query(Customer).all()
        display_customers(customers)

        contracts = session.query(Contract).all()
        display_contracts(contracts)

        events = session.query(Event).all()
        display_events(events)


@cli.command()
@pass_context
def create_customer(ctx):
    """Create a new customer."""
    if sales_permission(ctx):
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


@cli.command()
@pass_context
def update_customer(ctx, customer_id):
    """Update a customer."""
    if sales_permission(ctx):
        customer = session.query(Customer).filter_by(id=customer_id).first()

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

            customer.first_name = first_name
            customer.last_name = last_name
            customer.email = email
            customer.phone = phone
            customer.company_name = company_name

            session.commit()
            print("[bold green]Customer updated successfully[/bold green].")
        else:
            print("[bold red]No customer found.[/bold red]")


@cli.command()
@pass_context
def delete_customer(ctx, customer_id):
    """Delete contract."""
    if sales_permission(ctx):
        customer = session.get(Customer, customer_id)

        if customer and customer.sales_contact_id == ctx.user.id:
            click.echo("Deleting customer")

            contracts = session.query(Contract).filter_by(customer_id=customer.id).all()
            for contract in contracts:
                events = session.query(Event).filter_by(contract_id=contract.id).all()
                for event in events:
                    session.delete(event)

                session.delete(contract)

            session.delete(customer)
            session.commit()
            print("[bold green]Customer deleted successfully[/bold green].")
        else:
            print("[bold red]Customer not found.[/bold red]")


@cli.command()
@pass_context
def create_contract(ctx, id_customer):
    """Create a new contract."""
    if management_permission(ctx):
        customer = session.query(Customer).filter_by(id=id_customer).first()
        if customer:
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
            if is_signed:
                sentry_sdk.capture_message("Contract signed !")
            print("[bold green]Contract created successfully[/bold green].")
        else:
            print("[bold red]Customer not found.[/bold red]")


@cli.command()
@pass_context
def update_contract(ctx, contract_id):
    """Update a contract."""
    if management_permission(ctx):
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
            if is_signed:
                sentry_sdk.capture_message("Contract signed !")
            print("[bold green]Contract updated successfully[/bold green].")
        else:
            print("[bold red]Contract not found.[/bold red]")


@cli.command()
@pass_context
def delete_contract(ctx, contract_id):
    """Delete contract."""
    if management_permission(ctx):
        contract = session.get(Contract, contract_id)

        if contract and contract.management_contact_id == ctx.user.id:
            click.echo("Deleting contract")

            events = session.query(Event).filter_by(contract_id=contract.id).all()
            for event in events:
                session.delete(event)

            session.delete(contract)
            session.commit()
            print("[bold green]Contract deleted successfully[/bold green].")
        else:
            print("[bold red]Contract not found or Permission denied[/bold red].")


@cli.command()
@pass_context
def create_event(ctx, id_contract):
    """Create a new event."""
    if sales_permission(ctx):
        contract = session.get(Contract, id_contract)
        if contract:
            if contract.is_signed is True:
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
            else:
                print("[bold red]Contract no signed[/bold red].")
        else:
            print("[bold red]Contract not found.[/bold red]")


@cli.command()
@pass_context
def update_event(ctx, event_id):
    """Update event and Assign support event."""
    current_datetime = datetime.now()
    user_role = ctx.user.role.name
    user_id = ctx.user.id
    try:
        if user_role in ["support", "management"]:
            event = session.get(Event, event_id)
            if event:
                if event.event_date_end > current_datetime:
                    if user_role == "support" and event.support_contact_id == user_id:
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
                        notes = click.prompt(
                            "Event Notes", default=event.notes, type=str
                        )

                        event.event_name = event_name
                        event.event_date_start = event_date_start
                        event.event_date_end = event_date_end
                        event.location = location
                        event.attendees = attendees
                        event.notes = notes
                        session.commit()
                        print("[bold green]Event operation completed[/bold green].")

                    elif user_role == "management":
                        click.echo(f"Assign support event: {event.event_name}:")
                        support_email = click.prompt(
                            "Enter Support Contact Email", type=str
                        )
                        support_user = (
                            session.query(User)
                            .filter_by(email=support_email, role="support")
                            .first()
                        )

                        if support_user:
                            event.support_contact_id = support_user.id
                            session.commit()
                            print("[bold green]Event operation completed[/bold green].")
                        else:
                            print(
                                f"[bold red]{support_email} is not a support user. Support contact not assigned.[/bold red]"
                            )
                    else:
                        raise ValueError("No support user assigned.")
                else:
                    raise ValueError("Unable to update. The event has already ended.")
            else:
                raise ValueError("Event not found.")
        else:
            raise ValueError("User does not have the required role for this operation.")

    except ValueError as e:
        print(f"[bold red]Error : {e}[/bold red]")


@cli.command()
@pass_context
def delete_event(ctx, event_id):
    """Delete event."""
    if support_permission(ctx):
        event = session.get(Event, event_id)

        if event and event.support_contact_id == ctx.user.id:
            click.echo(f"Deleting event: {event.event_name}")
            session.delete(event)
            session.commit()
            print("[bold green]Event deleted successfully[/bold green].")
        else:
            print("[bold red]Event not found.[/bold red]")


if __name__ == "__main__":
    sentry_dsn = os.environ.get("SENTRY_DSN")
    sentry_sdk.init(
        # dsn="https://218fd0708459e9f02f9fa094de9ce64d@o4506610879954944.ingest.sentry.io/4506610888540160",
        dsn=sentry_dsn,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )
    cli()
