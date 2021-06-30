<!-- markdownlint-disable -->
<p align="center">
  <a href="https://bhagavadgita.io">
    <img src=".github/gita.png" alt="Logo" width="300">
  </a>

  <h3 align="center">Bhagavad Gita API v2</h3>

  <p align="center">
    Code for the BhagavadGita.io v2 API, which is an app built for Gita readers by Gita readers.
    <br />
    <br />
    <img alt="GitHub issues" src="https://img.shields.io/github/issues/gita/bhagavad-gita-api">
    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/bhagavad-gita-api">
      <a href="https://github.com/gita/bhagavad-gita-api/blob/master/LICENSE">
    <img alt="LICENSE" src="https://img.shields.io/badge/License-MIT-yellow.svg?maxAge=43200">
  </a>
  <a href="https://api.bhagavadgita.io/docs"><img src="https://img.shields.io/badge/docs-passing-green" alt="Docs"></a>
  <a href="https://starcharts.herokuapp.com/gita/bhagavad-gita-api"><img alt="Stars" src="https://img.shields.io/github/stars/gita/bhagavad-gita-api.svg?style=social"></a>
</p>


## Usage

The Bhagavad Gita API allows any developer to use content from Gita in their apps.
This API is built with FastAPI which is based on (and fully compatible with) the open standards for APIs: OpenAPI (previously known as Swagger) and JSON Schema.

Documentation for this API is availaible in two interactive formats:
- [Swagger UI](https://api.bhagavadgita.io/docs)
- [Redoc](https://api.bhagavadgita.io/redoc)

If you are interested in using this API for your application, you need to obtain an API Key from [bhagavadgita.io](https://bhagavadgita.io).

## Projects

Here is a list of interesting projects using this API.

- [bhagavadGita.io](https://bhagavadgita.io)
- [Android App](https://play.google.com/store/apps/details?id=com.hanuman.bhagavadgita)

Have you build something with this API ? Open a "Show and tell" discussion. The maintainers will feature your project on the README if they find it interesting.

## Self Hosting
<!-- markdownlint-enable -->

The official API at [api.bhagavadgita.io](https://api.bhagavadgita.io)
is free to use for all.
But If you wish you can self host anywhere you want.

If you want to deploy your own instance,You can deploy
the API server on your system or VPS.

- Using [`pipx`](https://pypa.github.io/pipx/installation/)
  > **Note** If you dont have `pipx`, just `pip install pipx`

    ```shell
    pipx run bhagavad-gita-api
    ```

- Or using [`docker`](https://www.docker.com/)

    ```shell
    docker run -it -p 8081:8081 --env-file=.env bhagavadgita/bhagavad-gita-api
    ```

<!-- markdownlint-disable -->
Now open http://localhost:8081/docs to see docs.
To stop the server press <kbd>Ctrl</kbd> + <kbd>C</kbd> on your keyboard.
<!-- markdownlint-enable -->

By default an in-memory SQLite database is used.
But you configure to use any SQL database of your choice.
The official version uses PostgreSQL.

Looking to deploy on a cloud platform ?
We have detailed docs to deploy to the following platforms:

- [Heroku](https://github.com/gita/bhagavad-gita-api/wiki/Heroku)
- [Deta](https://github.com/gita/bhagavad-gita-api/wiki/Deta)
- [Digital Ocean](https://github.com/gita/bhagavad-gita-api/wiki/Digial-Ocean)

## Configuration

Here is the list of supported environment variables.

<!-- markdownlint-disable -->
| Name                      | Description                           | Default     |
| ------------------------- | ------------------------------------- | ----------- |
| `TESTER_API_KEY`          | The API key for testing.              | `None`      |
| `SQLALCHEMY_DATABASE_URI` | The DSN for your database connection. | `sqlite://` (in memory SQLite db)|
<!-- markdownlint-enable -->

If you want to configure your deployment even more,
then please take a look at module [`config.py`](bhagavad_gita_api/config.py).

To set the environment variables, you may simply use a `.env` file where you
specify the values in the format of `KEY=VALUE`.

## Development

Feel free to use the [issue tracker](https://github.com/gita/bhagavad-gita-api/issues)
for bugs and feature requests.

Looking to contribute code ? PRs are most welcome!
To get started with developing this API, please read the [contributing guide](.github/CONTRIBUTING.md).

## Community

Join the [Discord chat server](https://discord.gg/gX8dstApZX) and
hang out with others in the community.

You can also use [GitHub Discussions](https://github.com/gita/bhagavad-gita-api/discussions)
to ask questions or tell us about
projects you have built using this API.
