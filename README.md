<p align="center">
  <a href="https://bhagavadgita.io">
    <img src="https://raw.githubusercontent.com/gita/bhagavad-gita-api/main/.github/gita.png" alt="Logo" width="300">
  </a>

  <h3 align="center">Bhagavad Gita API</h3>

  <p align="center">
    The Bhagavad Gita API is a tool created by Gita enthusiasts for Gita enthusiasts. It provides access to the content of the Bhagavad Gita for developers to integrate into their applications.
    <br />
    <br />
    <img alt="GitHub issues" src="https://img.shields.io/github/issues/gita/bhagavad-gita-api">
    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/bhagavad-gita-api">
      <a href="https://github.com/gita/bhagavad-gita-api/blob/master/LICENSE">
    <img alt="LICENSE" src="https://img.shields.io/badge/License-MIT-yellow.svg?maxAge=43200">
  </a>
  <a href="https://github.com/gita/bhagavad-gita-api/actions/workflows/deploy.yml"><img alt="Stars" src="https://github.com/gita/bhagavad-gita-api/actions/workflows/deploy.yml/badge.svg"></a>
  <a href="https://api.bhagavadgita.io/docs"><img src="https://img.shields.io/badge/docs-passing-green" alt="Docs"></a>
  <a href="https://starcharts.herokuapp.com/gita/bhagavad-gita-api"><img alt="Stars" src="https://img.shields.io/github/stars/gita/bhagavad-gita-api.svg?style=social"></a>
</p>


## Usage

The Bhagavad Gita API allows any developer to incorporate Gita content into their applications. This API is powered by FastAPI, which adheres to open standards for APIs such as OpenAPI (formerly known as Swagger) and JSON Schema.

You can access the API documentation in two interactive formats:
- [Swagger UI](https://api.bhagavadgita.io/docs)
- [Redoc](https://api.bhagavadgita.io/redoc)

If you're interested in using this API for your application, please register an account at [RapidAPI](https://rapidapi.com/bhagavad-gita-bhagavad-gita-default/api/bhagavad-gita3). You'll get both the necessary credentials and sample code in your preferred programming language. The API is completely free to use.

## Projects

Here is a list of interesting projects that utilize this API.

- [BhagavadGita.io](https://bhagavadgita.io)
- [Android App](https://play.google.com/store/apps/details?id=com.hanuman.bhagavadgita)

Have you built something with this API? Feel free to start a "Show and tell" discussion. The maintainers may feature your project on the README if they find it intriguing.

## Self Hosting

The official API is open for all to use. However, if you prefer, you can self-host it wherever you like.

To deploy your own instance of the API server, you have two options:

1. Using [`pipx`](https://pypa.github.io/pipx/installation/):
    > **Note**: If you don't have `pipx`, simply install it with `pip install pipx`.

    ```shell
    pipx run bhagavad-gita-api
    ```

2. Or using [`docker`](https://www.docker.com/):

    ```shell
    docker run -it -p 8081:8081 --env-file=.env bhagavadgita/bhagavad-gita-api
    ```

Now, open http://localhost:8081/docs in your web browser to access the API documentation. To stop the server, press <kbd>Ctrl</kbd> + <kbd>C</kbd> on your keyboard.

By default, the API uses an in-memory SQLite database, but you can configure it to use any SQL database of your choice. The official version employs PostgreSQL.

If you're looking to deploy on a cloud platform, we have detailed documentation for deployment on the following platforms:
- [Heroku](https://github.com/gita/bhagavad-gita-api/wiki/Heroku)
- [Deta](https://github.com/gita/bhagavad-gita-api/wiki/Deta)
- [Digital Ocean](https://github.com/gita/bhagavad-gita-api/wiki/Digial-Ocean)

## Configuration

Here is the list of supported environment variables:

| Name                      | Description                           | Default     |
| ------------------------- | ------------------------------------- | ----------- |
| `TESTER_API_KEY`          | The API key for testing.              | `None`      |
| `SQLALCHEMY_DATABASE_URI` | The Data Source Name (DSN) for your database connection. | `sqlite://` (in-memory SQLite database) |

If you want to configure your deployment further, please refer to the [`config.py`](bhagavad_gita_api/config.py) module.

To set the environment variables, you can use a `.env` file where you specify the values in the format of `KEY=VALUE`.

## Development

Feel free to use the [issue tracker](https://github.com/gita/bhagavad-gita-api/issues) for reporting bugs and suggesting new features.

If you want to contribute code, pull requests are more than welcome! To get started with developing for this API, please read the [contributing guide](.github/CONTRIBUTING.md).

## Community

Join the [Discord chat server](https://discord.gg/gX8dstApZX) to interact with others in the community.

You can also use [GitHub Discussions](https://github.com/gita/bhagavad-gita-api/discussions) to ask questions or showcase projects you've built using this API.

## Contributors ✨

A big thank you to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/Gupta-Anubhav12"><img src="https://avatars.githubusercontent.com/u/64721638?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Anubhav Gupta</b></sub></a><br /><a href="https://github.com/gita/bhagavad-gita-api/commits?author=Gupta-Anubhav12" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/sanujsood"><img src="https://avatars.githubusercontent.com/u/67072668?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Sanuj Sood</b></sub></a><br /><a href="https://github.com/gita/bhagavad-gita-api/commits?author=sanujsood" title="Code">💻</a></td>
    <td align="center"><a href="http://aahnik.dev"><img src="https://avatars.githubusercontent.com/u/66209958?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Aahnik Daw</b></sub></a><br /><a href="https://github.com/gita/bhagavad-gita-api/commits?author=aahnik" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/akshatj2209"><img src="https://avatars.githubusercontent.com/u/57488922?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Akshat Joshi</b></sub></a><br /><a href="https://github.com/gita/bhagavad-gita-api/commits?author=akshatj2209" title="Code">💻</a></td>
    <td align="center"><a href="https://www.realdevils.com/"><img src="https://avatars.githubusercontent.com/u/60562606?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Amritpal Singh</b></sub></a><br /><a href="https://github.com/gita/bhagavad-gita-api/commits?author=Amritpal2001" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/NIKU-SINGH"><img src="https://avatars.githubusercontent.com/u/72123526?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Niku Singh</b></sub></a><br /><a href="https://github.com/gita/bhagavad-gita-api/commits?author=NIKU-SINGH" title="Code">💻</a></td>
    <td align="center"><a href="https://sreevardhanreddi.github.io/"><img src="https://avatars.githubusercontent.com/u/31174432?v=4?s=100" width="100px;" alt=""/><br /><sub><b>sreevardhanreddi</b></sub></a><br /><a href="https://github.com/gita/bhagavad-gita-api/commits?author=sreevardhanreddi" title="Code">💻</a> <a href="#infra-sreevardhanreddi" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. We welcome contributions of all kinds!
