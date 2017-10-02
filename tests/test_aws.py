# -*- coding: utf-8 -*-
import pytest


@pytest.fixture
def aws_host():
    from ati.terraform import aws_host
    return aws_host


@pytest.fixture
def aws_resource():  # noqa
    return {
        "type": "aws_instance",
        "depends_on": ["aws_key_pair.deployer", "aws_security_group.control",
                       "aws_subnet.main", "aws_vpc.main"],
        "primary": {
            "id": "i-c99f6f60", "attributes": {
                "ami": "ami-fe100a96", "associate_public_ip_address": "true",
                "availability_zone": "us-east-1e", "ebs_block_device.#": "0",  # noqa
                "ebs_optimized": "false", "ephemeral_block_device.#": "0",
                "id": "i-c99f6f60", "instance_type": "m1.medium", "key_name":
                "key-mi", "private_dns": "ip-10-0-152-191.ec2.internal",
                "private_ip": "10.0.152.191", "public_dns":
                "ec2-52-7-74-115.compute-1.amazonaws.com", "public_ip":
                "52.7.74.115", "root_block_device.#": "1",
                "ebs_block_device.#": "1",  # noqa
                "ebs_block_device.3075786550.delete_on_termination": "false",
                "ebs_block_device.3075786550.device_name": "xvdh",
                "ebs_block_device.3075786550.encrypted": "false",
                "ebs_block_device.3075786550.iops": "300",
                "ebs_block_device.3075786550.snapshot_id": "",
                "ebs_block_device.3075786550.volume_size": "100",
                "ebs_block_device.3075786550.volume_type": "gp2",
                "root_block_device.0.delete_on_termination": "true",
                "root_block_device.0.iops": "18",
                "root_block_device.0.volume_size": "6",
                "root_block_device.0.volume_type": "gp2", "security_groups.#":
                "0", "subnet_id": "subnet-1155c03a", "tags.#": "4",
                "tags.Name": "mi-control-01", "tags.dc": "aws", "tags.role":
                "control", "tags.sshUser": "ec2-user", "tenancy": "default",
                "vpc_security_group_ids.#": "2",
                "vpc_security_group_ids.1636704399": "sg-9c360cf8",
                "vpc_security_group_ids.3543019159": "sg-9d360cf9"
            }, "meta": {"schema_version": "1"}  # noqa
        }
    }


def test_name(aws_resource, aws_host):
    name, _, _ = aws_host(aws_resource, '')
    assert name == 'mi-control-01'


@pytest.mark.parametrize('attr,should', {
    'ami': 'ami-fe100a96',
    'availability_zone': 'us-east-1e',
    'ebs_block_device': [{
        'delete_on_termination': 'false',
        'device_name': 'xvdh',
        'encrypted': 'false',
        'iops': '300',
        'snapshot_id': '',
        'volume_size': '100',
        'volume_type': 'gp2',
    }],
    'ebs_optimized': False,
    'ephemeral_block_device': [],
    'id': 'i-c99f6f60',
    'key_name': 'key-mi',
    'private': {'ip': '10.0.152.191', 'dns': 'ip-10-0-152-191.ec2.internal'},
    'public': {
        'ip': '52.7.74.115', 'dns': 'ec2-52-7-74-115.compute-1.amazonaws.com'
    },
    'role': 'control',
    'root_block_device': [{
        'volume_size': '6', 'iops': '18', 'delete_on_termination': 'true',
        'volume_type': 'gp2'
    }],
    'security_groups': [],
    'subnet': {'id': 'subnet-1155c03a'},
    'tags': {
        'sshUser': 'ec2-user', 'role': 'control', 'dc': 'aws', 'Name':
        'mi-control-01'
    },
    'tenancy': 'default',
    'vpc_security_group_ids': ['sg-9c360cf8', 'sg-9d360cf9'],
    # ansible
    'ansible_ssh_host': '52.7.74.115',
    'ansible_ssh_user': 'ec2-user',
    # mi
    'consul_dc': 'aws',
    # generic
    'private_ipv4': '10.0.152.191',
    'public_ipv4': '52.7.74.115',
    'provider': 'aws',
}.items())
def test_attrs(aws_resource, aws_host, attr, should):
    _, attrs, _ = aws_host(aws_resource, 'module_name')
    assert attr in attrs
    if type(attrs[attr]) == list:
        assert sorted(attrs[attr]) == sorted(should)
    else:
        assert attrs[attr] == should


@pytest.mark.parametrize(
    'group',
    ['aws_ami_ami_fe100a96', 'aws_az_us_east_1e', 'aws_key_name_key_mi',
     'aws_tenancy_default', 'aws_tag_sshUser_ec2_user', 'aws_tag_role_control',
     'aws_tag_dc_aws', 'aws_tag_Name_mi_control_01',
     'aws_vpc_security_group_sg_9c360cf8',
     'aws_vpc_security_group_sg_9d360cf9', 'aws_subnet_id_subnet_1155c03a',
     'role_control', 'dc_aws'])
def test_groups(aws_resource, aws_host, group):
    _, _, groups = aws_host(aws_resource, 'module_name')
    assert group in groups
