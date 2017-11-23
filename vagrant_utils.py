import shlex
from subprocess import run, Popen, STDOUT, PIPE
import os
from shutil import rmtree
import sys
from conditional import conditional
import pytest

deploy_path = 'deploy-test-dir'
vagrant_path = '{}/ubersystem-deploy/'.format(deploy_path)


@pytest.fixture(scope="session")
def vagrant_env(pytestconfig):
    # stdout capturing related stuff, so we can see the vagrant output
    capmanager = pytestconfig.pluginmanager.getplugin('capturemanager')

    capmanager.suspendcapture()
    setup_vagrant()
    capmanager.resumecapture()

    # go run the tests now.
    yield

    capmanager.suspendcapture()
    teardown_vagrant()
    capmanager.resumecapture()


def _run_shell_cmd(command_line, working_dir=None, disable_stdout_capture=True):
    args = shlex.split(command_line)
    process = Popen(args=args, cwd=working_dir, stdout=PIPE, stderr=STDOUT)
    while True:
        output = process.stdout.readline().decode()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    rc = process.poll()
    return rc


def _delete_dir(dir):
    assert deploy_path in dir
    rmtree(dir)  # use caution, will kill the universe


def setup_vagrant():
    teardown_vagrant()

    print("starting up a new vagrant environment")

    _run_shell_cmd('git clone https://github.com/magfest/simple-rams-deploy {}'.format(deploy_path))
    _run_shell_cmd('./install-unix.sh prime', deploy_path)


def teardown_vagrant():
    print("removing vagrant environment, if it exists")

    if os.path.isdir(deploy_path):
        if os.path.isdir(vagrant_path):
            _run_shell_cmd('vagrant destroy', vagrant_path)

        _delete_dir(deploy_path)