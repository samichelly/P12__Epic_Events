import click
from datetime import datetime, timedelta
from decimal import Decimal
from rich import print
from rich.console import Console
from rich.table import Table

from table import display_customers, display_contracts, display_events

# from customers import create_customer
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
        print("ctx.user : ", ctx)
        choices = [
            "create_user",
            "login",
            "exit",
        ]
        action = click.prompt("Select a choice", type=click.Choice(choices))

        if action == "create_user":
            ctx.invoke(create_user)
        elif action == "login":
            log_in = ctx.invoke(login)
            if log_in is True:
                ctx.invoke(authenticated_users)
        elif action == "exit":
            print("dans le exit")
            in_app = False
            break
        else:
            click.echo("Invalid action. Please choose a valid action.")


@cli.command()
@click.pass_context
def authenticated_users(ctx):
    """Main command to choose between various actions."""
    while True:
        key = click.prompt("Press a key + enter to load data")
        if key:
            print("Lists of Customers, Contracts and Events")
            ctx.invoke(lists_customers_contracts_events)

            choices = [
                "create-customer",
                "create-contract",
                "create-event",
                "update-contract",
                "update-customer",
                "update-event",
                "delete-customer",
                "delete-contract",
                "delete-event",
                "delete-user",
                "logout",
                "crash",
            ]

            action = click.prompt("Select a choice", type=click.Choice(choices))

            if action == "create-customer":
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
                ctx.invoke(delete_user)
            elif action == "logout":
                # ctx.user = None
                ctx.invoke(logout)
                # print("ctx_userrrr : ", ctx.user)
                # ctx.invoke(main)
                break
            elif action == "crash":
                main()
            else:
                click.echo("Invalid action. Please choose a valid action.")


@cli.command()
@pass_context
def login(ctx):
    """Authenticate a user."""
    print("ctx.user : ", ctx.user)
    email = click.prompt("Email", type=str)
    password = click.prompt("Password", type=str, hide_input=True)
    user = session.query(User).filter_by(email=email).first()

    if user and user.check_password(password):
        print(
            f"[bold green]Authentication successful[/bold green] for user with email {user.email}"
        )
        ctx.user = user
        print("context")
        print(ctx.user.email)
        return True
    else:
        print("Authentication failed.")


@cli.command()
@pass_context
def logout(ctx):
    """Logout a user."""
    print("in logout")
    ctx.user = None
    print("ctx_userrrr logout : ", ctx.user)


@cli.command()
# @pass_context
def create_user():
    """Create a new user."""
    click.echo("Creating a new user:")
    email = click.prompt("Email", type=str)
    password = click.prompt(
        "Password", type=str, hide_input=True, confirmation_prompt=True
    )
    first_name = click.prompt("First Name", type=str)
    last_name = click.prompt("Last Name", type=str)
    phone_number = click.prompt("Phone Number", type=str)
    role = click.prompt("Role", type=click.Choice(["sales", "support", "management"]))

    new_user = User(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        role=role,
    )
    session.add(new_user)
    session.commit()
    print("[bold green]User created successfully[/bold green].")
    # return new_user
    # main()


@cli.command()
@pass_context
def delete_user(ctx):
    """Delete user."""
    user_to_delete = session.query(User).get(ctx.user.id)

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

            for contract in user_to_delete.contract_management:
                contract.management_contact_id = replacement_user.id

            for event in user_to_delete.event_support:
                event.support_contact_id = replacement_user.id

            session.commit()

            print(f"[bold green]User deleted successfully[/bold green].")
        else:
            print(
                f"[bold red]No remplacement user. Please create a new user with same role[/bold red]."
            )


@cli.command()
@pass_context
def lists_customers_contracts_events(ctx):
    """List all customers, contracts, events."""
    if read_permission(ctx):
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
    print("dans la création de client")
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

            # Update customer fields
            customer.first_name = first_name
            customer.last_name = last_name
            customer.email = email
            customer.phone = phone
            customer.company_name = company_name

            session.commit()
            print("[bold green]Customer updated successfully[/bold green].")
        else:
            print("No customer found.")


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
            click.echo("Customer not found or Permission denied.")


@cli.command()
@pass_context
def create_contract(ctx, id_customer):
    """Create a new contract."""
    if management_permission(ctx):
        customer = session.query(Customer).filter_by(id=id_customer).first()

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
            print("[bold green]Contract updated successfully[/bold green].")
        else:
            print("[bold red]Contract not found or Permission denied[/bold red].")


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
                            click.echo(
                                "[bold green]Event operation completed[/bold green]."
                            )
                        else:
                            click.echo(
                                f"{support_email} is not a support user. Support contact not assigned."
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
        click.echo(f"Error : {e}")


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
            click.echo("Event not found or Permission denied.")


if __name__ == "__main__":
    cli()
