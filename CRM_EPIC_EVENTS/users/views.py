import bcrypt
import click
from models import User, Customer, Contract, Event, session
from datetime import datetime, timedelta


class Context:
    def __init__(self):
        self.user = None  # Stocker l'utilisateur authentifié


pass_context = click.make_pass_decorator(Context, ensure=True)


@click.group()
@click.pass_context
def cli(context):
    """CRM Epic Events"""
    context.obj = Context()


@cli.command()
@pass_context
def login(context):
    """Authenticate a user."""
    email = click.prompt("Email", type=str)
    password = click.prompt("Password", type=str, hide_input=True)

    user = authenticate_user(email, password)

    if user:
        print(f"Authentication successful for user with email {user.email}")
        context.obj.user = user
    else:
        print("Authentication failed.")


@cli.command()
def input_new_user():
    """Create a new user."""
    click.echo("Creating a new user:")
    email = click.prompt("Email", type=str)
    password = click.prompt(
        "Password", type=str, hide_input=True, confirmation_prompt=True
    )
    first_name = click.prompt("First Name", type=str)
    last_name = click.prompt("Last Name", type=str)
    role = click.prompt("Role", type=click.Choice(["sales", "support", "management"]))

    create_user(email, password, first_name, last_name, role)
    print("User created successfully.")


def authenticate_user(email, password):
    user = session.query(User).filter_by(email=email, password=password).first()

    if user:
        # if user and bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        print(f"Successful login for user with email {email}")
        return user
    else:
        print(f"Login failed for user with email {email}")
        return False


@cli.command()
def create_user(email, password, first_name, last_name, role):
    """Create a new user."""
    new_user = User(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        role=role,
    )

    session.add(new_user)
    session.commit()
    print("User created successfully")
    return


@cli.group()
@pass_context
def authenticated_users(context):
    """Commands for authenticated users"""
    pass


@authenticated_users.command()
def list_customers():
    """List all customers."""
    customers = session.query(Customer).all()

    if not customers:
        print("No customers found.")
        return

    print("List of customers:")
    for customer in customers:
        print(f"{customer.first_name} {customer.last_name} - {customer.email}")


@authenticated_users.command()
def list_contracts():
    """List all contracts."""
    # ... (code to list all contracts)


@authenticated_users.command()
def list_events():
    """List all events."""
    # ... (code to list all events)


@authenticated_users.command()
def input_new_customer():
    """Create a new customer."""
    click.echo("Creating a new customer:")
    first_name = click.prompt("Customer First Name", type=str)
    last_name = click.prompt("Customer Last Name", type=str)
    email = click.prompt("Customer Email", type=str)
    phone = click.prompt("Customer Phone", type=str)
    company_name = click.prompt("Customer Company Name", type=str)

    create_customer(first_name, last_name, email, phone, company_name)
    print("Customer created successfully.")

    # return first_name, last_name, email, phone, company_name


@click.command()
def create_customer(first_name, last_name, email, phone, company_name):
    """Create a new customer."""
    new_customer = Customer(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        company_name=company_name,
        # sales_contact=new_user,
    )

    session.add(new_customer)
    session.commit()
    print("Customer created successfully")


cli.add_command(authenticated_users)

if __name__ == "__main__":
    cli()
