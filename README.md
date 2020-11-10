## CLI Weather API
Python CLI made with Click using the OpenWeatherMap API
showing the current weather in a given location

You can run .exe or .py file **in the terminal** with parameters 
or without parameters to see the help message.

1. Create a free account at https://openweathermap.org/appid
2. Configure your API key with 'config' command
3. Check current weather with 'current' command providing the city name (inside "" if the name consists of multiple words, like "Rio de Janeiro")

Options:
```
-a, --api-key API-KEY  : your API key for the OpenWeatherMap API
-c, --config-file PATH : path to the configuration file containing API key
--help                 : Show this message and exit.
```

Commands:
```
config   Store configuration value (API key for OpenWeatherMap) in a file.
current  Show the current weather for a given location using OpenWeatherMap.
```
