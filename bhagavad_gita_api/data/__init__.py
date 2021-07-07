"""
    Load initial data into database.

   isort:skip_file
"""
import os


def insert_all():
    """Insert data from github.com/gita/gita into database."""

    from bhagavad_gita_api.data.insert import (
        authors,
        languages,
        chapters,
        verses,
        translations,
        commentaries,
    )

    # importing the modules executes the code in it
