<!-- markdownlint-disable -->
<p align="center">
  <a href="https://bhagavadgita.io">
    <img src="https://raw.githubusercontent.com/gita/bhagavad-gita-api/main/.github/gita.png" alt="Logo" width="300">
  </a>

  <h3 align="center">Bhagavad Gita API</h3>

  <p align="center">
    Code for the BhagavadGita.io API, which is an app built for Gita readers by Gita readers.
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

The Bhagavad Gita API allows any developer to use content from Gita in their apps.
This API is built with FastAPI which is based on (and fully compatible with) the open standards for APIs: OpenAPI (previously known as Swagger) and JSON Schema.

Documentation for this API is availaible in two interactive formats:
- [Swagger UI](https://api.bhagavadgita.io/docs)
- [Redoc](https://api.bhagavadgita.io/redoc)

If you are interested in using this API for your application, please
register an account at
[RapidAPI](https://rapidapi.com/bhagavad-gita-bhagavad-gita-default/api/bhagavad-gita3)
where you'll get both the credentials as well as sample code in your language of
choice. The API is 100% FREE to use.

## Projects

Here is a list of interesting projects using this API.

- [BhagavadGita.io](https://bhagavadgita.io)
- [Android App](https://play.google.com/store/apps/details?id=com.hanuman.bhagavadgita)

Have you ever thought of building anything with this API ? Open a "Show and tell" discussion. The maintainers will feature your project on the README file if they find it interesting.

## Self Hosting
<!-- markdownlint-enable -->

The official API is free to use for all.
But If you wish you can self host anywhere you want.

If you want to deploy your own instance, you can deploy
the API server on your system or VPS.

- Using [`pipx`](https://pypa.github.io/pipx/installation/)
  > **Note** If you don't have `pipx`, just run `pip install pipx` command

    ```shell
    pipx run bhagavad-gita-api
    ```

- Or use [`docker`](https://www.docker.com/)

    ```shell
    docker run -it -p 8081:8081 --env-file=.env bhagavadgita/bhagavad-gita-api
    ```

<!-- markdownlint-disable -->
Now open http://localhost:8081/docs to see docs.
To stop the server, press <kbd>Ctrl</kbd> + <kbd>C</kbd> on your keyboard.
<!-- markdownlint-enable -->

By default an in-memory SQLite database is used.
But you may configure any SQL database of your choice to use.
The official version uses PostgreSQL.

Looking to deploy on a cloud platform ?
We have detailed docs to deploy on the following platforms:

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

If you want to configure your deployment with more details,
then you may have a look at module [`config.py`](bhagavad_gita_api/config.py).

To set the environment variables, you may simply use a `.env` file where you will
specify the values in the format of `KEY=VALUE`.

## Development

Feel free to use the [issue tracker](https://github.com/gita/bhagavad-gita-api/issues)
for bugs and feature requests.

Looking to contribute code ? PRs are most welcome!
To get started with developing this API, please read the [contributing guide](.github/CONTRIBUTING.md).

## Community

Join the [Discord chat server](https://discord.gg/gX8dstApZX) and
hang out with other fellow Bhagvad Gita readers in the community.

You can also use [GitHub Discussions](https://github.com/gita/bhagavad-gita-api/discussions)
to ask questions or tell us about
projects you have built using this API.

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

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

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors)
specification. Contributions of any kind welcome!
