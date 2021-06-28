#!/usr/bin/env bash

python initial_data.py
python -m scripts.insert_authors
python -m scripts.insert_languages
python -m scripts.insert_chapters
python -m scripts.insert_verses
python -m scripts.insert_commentaries
python -m scripts.insert_translations
python -m scripts.insert_reference_verse_into_chapters
python -m scripts.insert_references_translations
python -m scripts.insert_references_commentaries
