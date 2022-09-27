import os

import click
import streamlit_authenticator as stauth
from deta import Deta
from dotenv import load_dotenv

load_dotenv(".env")
DETA_KEY = os.getenv("DETA_KEY")

deta = Deta(DETA_KEY)
users = deta.Base("users")


@click.group()
def cli():
    pass


@click.command("insert_user")
@click.argument("username")
@click.argument("password")
def insert_user(username, password):
    hased_password = stauth.Hasher([password]).generate()
    return users.put({"key": username, "password": hased_password[0]})


def get_users():
    res = users.fetch()
    return res.items


@click.command("get_user")
@click.argument("username")
def get_user(username):
    user = users.get(username)
    click.echo(f"{user}")
    return user


@click.command("delete_user")
@click.argument("username")
def delete_user(username):
    res = users.delete(username)
    click.echo(f"{res}")
    return res


cli.add_command(insert_user)
cli.add_command(delete_user)
cli.add_command(get_user)


if __name__ == "__main__":
    cli()
