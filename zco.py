import click
import boto3
from pssh.pssh_client import ParallelSSHClient
import json
import subprocess
import pprint
import os
from time import sleep


class InstanceList(object):

    def __init__(self, name=None, role=None, role_type=None, env=None):
            self.filter_options = {
                'Name': name,
                'Role': role,
                'RoleType': role_type,
                'Env': env,
            }
            self.filters = self._buildFilters()

    def list_by_tag(self, tag_name='Name'):
        tag_values = map(
            lambda instance: next(
                (tag['Value'] for tag in instance['Tags'] if tag['Key'] == tag_name),
                None
            ),
            self.getInstanceList()
        )
        return tag_values

    def getInstanceList(self):
        client = boto3.client('ec2')
        response = client.describe_instances(
            Filters=self.filters
        )
        instances = map(
            lambda reservation:
                reservation['Instances'][0], response['Reservations']
        )
        return instances

    def _buildFilters(self):
        filters = map(
            lambda kv: {
                'Name': 'tag:' + kv[0], 'Values': [kv[1]]
            },
            self.filter_options.items()
        )
        filters = [x for x in filters if x['Values'] != [None]]
        return filters


@click.group()
@click.option('-n', '--name', required=False, help='hostname to filter by')
@click.option('-r', '--role', required=False, help='role to filter by')
@click.option('-rt', '--roletype', required=False, help='roletype to filter by')
@click.option('-e', '--env', required=False, help='env to filter by')
@click.pass_context
def cli(context, name, role, roletype, env):
    context.obj = InstanceList(name, role, roletype, env)


@click.command()
@click.pass_context
@click.option('-v', '--verbose/--no-verbose', default=False)
def list(context, verbose):
    """List all ec2 instances by name."""
    instance_names = context.obj.list_by_tag()
    # json.dumps(context.obj.list, sort_keys=True, indent=4)
    click.echo('\n'.join(sorted(instance_names)))


@click.command()
@click.pass_context
@click.option('-c', '--command', default='hostname')
def run(context, command):
    """Run command across multiple servers."""
    hosts = [
        instance_name
        for instance_name in context.obj.list_by_tag('Name')
    ]
    client = ParallelSSHClient(hosts)
    output = client.run_command(command)
    # click.echo(json.dumps(output, indent=4))
    results = [
        '\n'.join([line for line in output[host]['stdout']])
        for host in output
    ]
    click.echo(results)

@click.command()
@click.pass_context
def update_autocomplete(context):
    """Update ssh autocomplete file."""
    with open(os.path.expanduser('~/.ssh/chartboost_hosts'), 'r+') as hosts_file:
        old_count = sum(1 for line in hosts_file)
    with open(os.path.expanduser('~/.ssh/chartboost_hosts'), 'w+') as hosts_file:
        instance_names = context.obj.list_by_tag('Name')
        hostnames = [
            instance_name + '.caffeine.io'
            for instance_name in instance_names
        ]
        hosts_file.write('\n'.join(hostnames) + '\n')
    new_count = len(hostnames)
    click.echo('Successfully updated autocomplete hosts list!')
    click.echo(
        'Previous host count: ' + click.style(str(new_count), fg='red') +
        '\nNew host count: ' + click.style(str(new_count), fg='green')
    )


@click.command()
def install_autocomplete():
    """Configure ssh autocomplete."""
    directory = os.path.expanduser('~/.bash_completion/')
    if not os.path.exists(directory):
        os.makedirs(directory)
    source = os.path.dirname(os.path.realpath(__file__)) + '/autocomplete.sh'
    destination = os.path.expanduser('~/.bash_completion/autocomplete.sh')
    os.symlink(source, destination)


cli.add_command(list)
cli.add_command(run)
cli.add_command(install_autocomplete)
cli.add_command(update_autocomplete)


# @click.group()
# @click.option('--Name', required=False)
# @click.option('--Role', required=False)
# @click.option('--RoleType', required=False)
# @click.option('--Env', required=False)
# def cli(context, name, role, role_type, env):
#     context.obj = Instances(name, role, role_type, env)
#
# @cli.command()
# @click.argument('--command', required=False, default='hostname')
# def run(command):
#     click.echo('Fooing')
