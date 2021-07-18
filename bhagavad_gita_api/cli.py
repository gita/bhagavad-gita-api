import typer

from bhagavad_gita_api.db.base_class import Base
from bhagavad_gita_api.db.init_db import init_db
from bhagavad_gita_api.db.session import SessionLocal, engine

app = typer.Typer()


@app.command()
def delete_all_data():
    """
    deletes all data
    """
    response = typer.prompt("Are you sure you want to delete all the data? [y/n]")
    if response == "y":
        typer.echo("Deleting...")
        Base.metadata.drop_all(bind=engine)
        typer.echo("Deleted.")


@app.command()
def seed_data():
    """
    seeds data to database
    """
    typer.echo("Creating initial data")
    db = SessionLocal()
    init_db(db)
    typer.echo("Initial data created")


if __name__ == "__main__":
    app()
