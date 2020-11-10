import click
import requests
import os
import re

SAMPLE_API_KEY = 'b1b15e88fa797225412429c1c50c122a1'

# class to build custom parameter type to validate user input


class ApiKey(click.ParamType):
    name = 'api-key'

    def convert(self, value, param, ctx):
        found = re.match(r'[0-9a-f]{32}', value)

        if not found:
            self.fail(
                f'{value} is not a 32-character hexadecimal string',
                param,
                ctx
            )

        return value


def current_weather(location, api_key=SAMPLE_API_KEY):
    url = 'https://api.openweathermap.org/data/2.5/weather?'

    query_params = {
        'q': location,
        'appid': api_key,
    }

    response = requests.get(url, params=query_params)

    return response.json()['weather'][0]['description']


@click.group()
@click.option(
    '--api-key', '-a',
    type=ApiKey(),
    help='your API key for the OpenWeatherMap API'
)
@click.option(
    '--config-file', '-c',
    type=click.Path(),
    default='~/.weather.cfg',
    help='path to the configuration file containing API key'
)
@click.pass_context
def main(ctx, api_key, config_file):
    """
    A little weather tool that shows you the current weather in a LOCATION of
    your choice. Provide the city name (London or "Rio de Janeiro")
    as well as a valid API key from OpenWeatherMap for the tool to work. You can
    sign up for a free account at https://openweathermap.org/appid.
    """
    filename = os.path.expanduser(config_file)

    if not api_key and os.path.exists(filename):
        with open(filename) as cfg:
            api_key = cfg.read()

    ctx.obj = {
        'api_key': api_key,
        'config_file': filename
    }


# We turned main function into a command group object
# that we can use to register new commands “below” it.
# So we change @click.command to @main.command
# and function name will be the name of the command.


@main.command()
@click.pass_context
def config(ctx):
    """
    Store configuration value (API key for OpenWeatherMap) in a file.
    """
    config_file = ctx.obj['config_file']

    api_key = click.prompt(
        'Please enter your API key',
        default=ctx.obj.get('api_key', ''),
        type=ApiKey()
    )

    with open(config_file, 'w') as cfg:
        cfg.write(api_key)


# alternative to configuration file would be envvar parameter:
    # envvar="API_KEY"  # -  not to type api key each time you can
    # make it a temporary environment variable by running:
    # on Windows: >set API_KEY=641b4cf91d5af69830e3b37b333326d4
    # on Linux: $export API_KEY="641b4cf91d5af69830e3b37b333326d4"
    # before calling the cli


@main.command()
@click.argument('location')
@click.pass_context
def current(ctx, location):
    """
    Show the current weather for a given location using OpenWeatherMap
    """
    api_key = ctx.obj['api_key']

    weather = current_weather(location, api_key)
    print(f"The weather in {location} right now: {weather}")


if __name__ == '__main__':
    main()
