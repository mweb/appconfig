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

## Installation

```
pip install appconfig
```

### Dependencies

The following packages are required for using the library:

* [appdirs](https://pypi.python.org/pypi/appdirs)

To run the unit test the following packages are required:

* [nose](https://nose.readthedocs.org/en/latest/)

## Examples 

### Example Config File

The config files that the user will use for your application will have the ini
format. For the application it self it is necessary to create a config file
with json content that allows to set the default values and the documentation
for all keys.

**Example JSON File**
```
{
    "application_name": "appconfig_test",
    "application_author": "python",
    "application_version": "1.0",
    "appconfig": {
        "first": {
            "default": 1,
            "description": "the first parameter",
            "type": "int"
        }
    }
}
```

This will lead to the following user config file:

**Example ini config File**
```
[appconfig]
# the first paramter 
# Type: [int]
# first = 1
fisrt = 10
```

## Example Usage

With the application and the user config from above a simple python
application might look like these:

```
#!/bin/env python

from appconfig import AppConfig


def main():
    """ The main method to be run.
    """
    conf = AppConfig()
    conf.init_default_config('example.json')
    conf.load('example.conf')

    value = conf.get_s('appconfig', 'first')
    print value
    print type(value)


if __name__ == '__main__':
    main()
```

## Application Config Format

The application config format is a simple config file with json syntax it
requires at least the application_name to be defined and one json object 
(config section) with at least one parameter defined.

```
{
    "application_name": "appconfig_test",
    "application_author": "python",
    "application_version": "1.0",
    "appconfig": {
        "first": {
            "default": 1,
            "description": "the first parameter",
            "type": "int"
        }
    }
}
```

* **application_name** Defines the application name for the application using
    this config file. The application name is used to access the global and
    the user local config files. (See Config File Location)
* **application_author** Defines the name of the author of the application.
    This name is used to access the user config file on Windows (See Config 
    File Location)
* **application_version** Defines the application version to separate
    different versions of the config file to support multiple versions of the
    same application on one system. (See Config File Location)
* **appconfig** Defines a section named `appconfig` The section name can be
    almost any name. Only the `application_*` keywords and the name hidden
    are prohibited since they are used from the library. It is possible to
    have multiple sections.

A section consists out of at least one parameter. Each parameter must be a json
object with the following three parameter defined:

* **default** This defines the default value that is used if the value is not
    set by the user.
* **description** Describes the parameter
* **type** Defines the type that this parameter gets converted to (see 
    Supported Types)

### Config File Location

The load_default function tries to load config files from different locations.
The first location it tries is the global config directory:

**Mac OS X**
```
/Library/Application Support/APPNAME/APPNAME.conf
```

**Linux**
```
/etc/xdg/APPNAME/APPNAME.conf
```

**Windows 7**
```
?
```

The second location is the users home directory where the local config files
are store.

**Mac OS X**
```
/Users/USERNAME/Library/Application Support/APPNAME/APPNAME.conf
```

**Linux**
```
/home/USERSNAME/.config/APPNAME/APPNAME.conf
```

**Windows**
```
C:\Users\USERNAME\AppData\Local\AUTHOR\APPNAME\APPNAME.conf
```

If both file exist they will be loaded in this order and the user config file
will override values from the global config file.

If the application version is specified then the application version will be
added to the path after the application name. This allows a per-version
isolation of the config files.

The `save` saves a config file if no config file is specified it will try to
use the user default location or the location configured within the section
`APPNAME` config value `config_file`.

### Suported Types

Currently the following types are supported for a config value:

* `str`
* `unicode`
* `int`
* `float`
* `bool`

All the types will be converted with python functions. The only exception is
the `bool` type. The boolean type uses the RawConfigParser.getboolean function.
This translates the following string to a true (1, yes, true, on)
