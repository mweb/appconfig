# appconfig

`appconfig` is a python module that simplifies the usage of ini based config
files. It uses the Python ConfigParser module. The advantage of the appconfig
module it that it allows defining default values for all config parameters and
to provide a description of each parameter. While writing the config file back
it will add comments above all of the config values and since we have default
values we never need to check if a value is defined.

## Features

The `appconfig` module offers the following features:

* default values for config values
* config file generation with parameter description
* automatic type conversion and type checks for config values
* config directory handling


