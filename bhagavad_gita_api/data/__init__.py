"""Load initial data into database."""
import os


def insert_all():
    """Insert data from github.com/gita/gita into database."""

    from bhagavad_gita_api.data.insert import (
        authors,
        chapters,
        commentaries,
        languages,
        translations,
        verses,
    )

    # importing the modules executes the code in it
