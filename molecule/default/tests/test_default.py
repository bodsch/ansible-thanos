# coding: utf-8
from __future__ import unicode_literals

from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar

import json
import pytest
import os

import testinfra.utils.ansible_runner

HOST = 'instance'

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts(HOST)


def pp_json(json_thing, sort=True, indents=2):
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(json_thing, sort_keys=sort, indent=indents))
    return None


def base_directory():
    """ ... """
    cwd = os.getcwd()

    if('group_vars' in os.listdir(cwd)):
        directory = "../.."
        molecule_directory = "."
    else:
        directory = "."
        molecule_directory = "molecule/{}".format(os.environ.get('MOLECULE_SCENARIO_NAME'))

    return directory, molecule_directory


def read_ansible_yaml(file_name, role_name):
    ext_arr = ["yml", "yaml"]

    read_file = None

    for e in ext_arr:
        test_file = "{}.{}".format(file_name, e)
        if os.path.isfile(test_file):
            read_file = test_file
            break

    return "file={} name={}".format(read_file, role_name)


@pytest.fixture()
def get_vars(host):
    """
        parse ansible variables
        - defaults/main.yml
        - vars/main.yml
        - vars/${DISTRIBUTION}.yaml
        - molecule/${MOLECULE_SCENARIO_NAME}/group_vars/all/vars.yml
    """
    base_dir, molecule_dir = base_directory()
    distribution = host.system_info.distribution

    if distribution in ['debian', 'ubuntu']:
        os = "debian"
    elif distribution in ['redhat', 'ol', 'centos', 'rocky', 'almalinux']:
        os = "redhat"
    elif distribution in ['arch']:
        os = "archlinux"

    # print(" -> {} / {}".format(distribution, os))
    # print(" -> {}".format(base_dir))

    file_defaults      = read_ansible_yaml("{}/defaults/main".format(base_dir), "role_defaults")
    file_vars          = read_ansible_yaml("{}/vars/main".format(base_dir), "role_vars")
    file_distibution   = read_ansible_yaml("{}/vars/{}".format(base_dir, os), "role_distibution")
    file_molecule      = read_ansible_yaml("{}/group_vars/all/vars".format(molecule_dir), "test_vars")
    # file_host_molecule = read_ansible_yaml("{}/host_vars/{}/vars".format(base_dir, HOST), "host_vars")

    defaults_vars      = host.ansible("include_vars", file_defaults).get("ansible_facts").get("role_defaults")
    vars_vars          = host.ansible("include_vars", file_vars).get("ansible_facts").get("role_vars")
    distibution_vars   = host.ansible("include_vars", file_distibution).get("ansible_facts").get("role_distibution")
    molecule_vars      = host.ansible("include_vars", file_molecule).get("ansible_facts").get("test_vars")
    # host_vars          = host.ansible("include_vars", file_host_molecule).get("ansible_facts").get("host_vars")

    ansible_vars = defaults_vars
    ansible_vars.update(vars_vars)
    ansible_vars.update(distibution_vars)
    ansible_vars.update(molecule_vars)
    # ansible_vars.update(host_vars)

    templar = Templar(loader=DataLoader(), variables=ansible_vars)
    result = templar.template(ansible_vars, fail_on_undefined=False)

    return result


def local_facts(host):
    """
      return local facts
    """
    return host.ansible("setup").get("ansible_facts").get("ansible_local").get("thanos")


@pytest.mark.parametrize("dirs", [
    "/etc/thanos",
])
def test_directories(host, dirs):
    d = host.file(dirs)
    assert d.is_directory
    assert d.exists


def test_files(host, get_vars):
    """
    """
    version = local_facts(host).get("version")

    install_dir = get_vars.get("thanos_install_path")
    defaults_dir = get_vars.get("thanos_defaults_directory")
    config_dir = get_vars.get("thanos_config_dir")

    if 'latest' in install_dir:
        install_dir = install_dir.replace('latest', version)

    files = []
    files.append("/usr/bin/thanos")

    if install_dir:
        files.append(f"{install_dir}/thanos")

    if defaults_dir:
        """
          every sub-service has an own config file
        """
        services = list(
            get_vars.get("thanos_services").keys()
        )

        for s in services:
            files.append(f"{defaults_dir}/thanos-{s}")

    if config_dir:
        files.append("{}/objstore.yml".format(config_dir))

    print(files)

    for _file in files:
        f = host.file(_file)
        assert f.exists
        assert f.is_file

def test_user(host, get_vars):
    """
    """
    user = get_vars.get("thanos_system_user", "thanos")
    group = get_vars.get("thanos_system_group", "thanos")

    assert host.group(group).exists
    assert host.user(user).exists
    assert group in host.user(user).groups
    assert host.user(user).home == "/nonexistent"


def test_service(host, get_vars):
    """
    """
    services = get_vars.get("thanos_services")

    for k, v in services.items():
        """
        """
        service_name = f"thanos@{k}"
        # _enabled = v.get('enabled', False)
        _state   = v.get('state', 'stopped')

        # print(f"service: {service_name}, enabled: {_enabled}, state: {_state}")

        service = host.service(service_name)
        # print(f"is_enabled: {service.is_enabled}")
        # print(f"is_running: {service.is_running}")
        # print("-------------------------------------------")

        # if _enabled:
        #     assert service.is_enabled
        # else:
        #     assert not service.is_enabled

        if _state == 'stopped':
            assert not service.is_running
        else:
            assert service.is_running

# def test_open_port(host, get_vars):
#     for i in host.socket.get_listening_sockets():
#         print(i)
#
#     thanos_service = get_vars.get("thanos_service", {})
#
#     print(thanos_service)
#
#     if isinstance(thanos_service, dict):
#         thanos_web = thanos_service.get("web", {})
#
#         listen_address = thanos_web.get("listen_address")
#     else:
#         listen_address = "0.0.0.0:9090"
#
#     service = host.socket("tcp://{0}".format(listen_address))
#     assert service.is_listening
