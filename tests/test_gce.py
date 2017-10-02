# -*- coding: utf-8 -*-
import pytest


@pytest.fixture
def gce_host():
    from ati.terraform import gce_host
    return gce_host


@pytest.fixture
def gce_resource():
    return {
        "type": "google_compute_instance",
        "depends_on": ["google_compute_network.mi-network"],
        "primary": {
            "id": "mi-control-01",
            "attributes": {
                "can_ip_forward": "false",
                "description": "mantl control node #01",
                "disk.#": "1",
                "disk.0.auto_delete": "true",
                "disk.0.device_name": "",
                "disk.0.disk": "",
                "disk.0.image": "centos-7-v20150423",
                "disk.0.scratch": "false",
                "disk.0.size": "0",
                "disk.0.type": "",
                "id": "mi-control-01",
                "machine_type": "n1-standard-1",
                "metadata.#": "3",
                "metadata.dc": "gce-dc",
                "metadata.role": "control",
                "metadata.sshKeys": "fake ssh key",
                "metadata_fingerprint": "RRQXhOpeylY=",
                "name": "mi-control-01",
                "network.#": "0",
                "network_interface.#": "1",
                "network_interface.0.access_config.#": "1",
                "network_interface.0.access_config.0.nat_ip": "104.197.63.156",
                "network_interface.0.address": "10.0.237.130",
                "network_interface.0.name": "nic0",
                "network_interface.0.network": "mantl",
                "self_link":
                "https://www.googleapis.com/compute/v1/projects/test-project/zones/us-central1-a/instances/mi-control-01",
                "service_account.#": "0",
                "tags.#": "2",
                "tags.2783239913": "mi",
                "tags.3990563915": "control",
                "tags_fingerprint": "hq1EeKIUnfk=",
                "zone": "us-central1-a"
            },
            "meta": {"schema_version": "2"}
        }
    }


def test_name(gce_resource, gce_host):
    name, _, _ = gce_host(gce_resource, '')
    assert name == 'mi-control-01'


@pytest.mark.parametrize('attr,should', {
    'can_ip_forward': False,
    'disks': [{
        'auto_delete': 'true',
        'device_name': '',
        'disk': '',
        'image': 'centos-7-v20150423',
        'scratch': 'false',
        'size': '0',
        'type': '',
    }],
    'machine_type': 'n1-standard-1',
    'metadata':
    {'dc': 'gce-dc',
     'role': 'control',
     'sshKeys': 'fake ssh key', },
    'network': [],
    'network_interface': [{
        'network': 'mantl',
        'access_config': [{'nat_ip': '104.197.63.156'}],
        'address': '10.0.237.130',
        'name': 'nic0'
    }],
    'self_link':
    'https://www.googleapis.com/compute/v1/projects/test-project/zones/us-central1-a/instances/mi-control-01',
    'service_account': [],
    'tags': ['mi', 'control'],
    'zone': 'us-central1-a',
    # ansible
    'ansible_ssh_host': '104.197.63.156',
    # mi
    'consul_dc': 'gce-dc',
    'role': 'control',
    'publicly_routable': True,
    # generic
    'private_ipv4': '10.0.237.130',
    'public_ipv4': '104.197.63.156',
    'provider': 'gce',
}.items())
def test_attrs(gce_resource, gce_host, attr, should):
    _, attrs, _ = gce_host(gce_resource, 'module_name')
    assert attr in attrs
    if type(attrs[attr]) == list:
        assert sorted(attrs[attr]) == sorted(should)
    else:
        assert attrs[attr] == should


@pytest.mark.parametrize('group', [
    'gce_image_centos_7_v20150423',
    'gce_machine_type_n1_standard_1',
    'gce_metadata_dc_gce_dc',
    'gce_metadata_role_control',
    'gce_tag_mi',
    'gce_tag_control',
    'gce_publicly_routable',
    'role_control',
    'dc_gce_dc',
])
def test_groups(gce_resource, gce_host, group):
    _, _, groups = gce_host(gce_resource, 'module_name')
    assert group in groups
