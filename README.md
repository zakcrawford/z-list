# ZCO

#### A Host discovery and batch remote-command execution utility

## Usage
```Bash
$ zco --help
Usage: zco [OPTIONS] COMMAND [ARGS]...

Options:
  -n, --name TEXT       hostname to filter by
  -r, --role TEXT       role to filter by
  -rt, --roletype TEXT  roletype to filter by
  -e, --env TEXT        env to filter by
  --help                Show this message and exit.

Commands:
  install_autocomplete  Configure ssh autocomplete.
  list                  List all ec2 instances by name.
  run                   Run command across multiple servers.
  update_autocomplete   Update ssh autocomplete file.
```

## Installation

### Dependencies
- Python 3
- pip
- virtualenv
- AWS Access Key ([How to set up AWS Access Keys](https://chartboost.atlassian.net/wiki/display/EN/AWS+Access+Keys))

### Configuration
```Bash
virtualenv -p python3 $HOME/virtualenv/zco
source ~/virtualenv/zco/bin/activate
sudo pip install --editable .
```

If you see an error regarding the version of `six` that came with the distutils in El Capitan, use the --ignore-installed option:

```Bash
sudo pip install --editable . --ignore-installed six
```
### SSH Autocompletion

Add this to to your ~/.bash_profile

```Bash
# Tab completion
for f in ~/.bash_completion/*; do source $f; done
```
