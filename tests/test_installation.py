"""
Role tests
"""

import pytest
from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner('.molecule/ansible_inventory').get_hosts('all')


@pytest.mark.parametrize('name', [
    ('clamav'),
    ('clamav-base'),
    ('clamav-daemon'),
])
def test_packages(host, name):
    """
    Check installed packages
    """

    assert host.package(name).is_installed


def test_service_user(host):
    """
    Check service user
    """

    service_user = host.user('clamav')

    assert service_user.exists
    assert service_user.home == '/var/lib/clamav'
    assert service_user.group == 'clamav'
    assert service_user.shell == '/bin/false'


def test_service_group(host):
    """
    Check service group
    """

    service_group = host.group('clamav')

    assert service_group.exists


@pytest.mark.parametrize('name', [
    ('clamd'),
    ('freshclam'),
])
def test_process(host, name):
    """
    Test process running
    """

    assert len(host.process.filter(user='clamav', comm=name)) == 1


@pytest.mark.parametrize('name', [
    ('clamav-daemon'),
    ('clamav-freshclam'),
])
def test_services(host, name):
    """
    Test services state
    """

    current_service = host.service(name)

    if host.system_info.codename == 'xenial':
        assert current_service.is_enabled
        assert current_service.is_running
    else:
        assert 'is running' in host.check_output(
            'service {} status'.format(name)
        )


@pytest.mark.parametrize('path_type,path,user,group,mode', [
    ('file', '/etc/clamav/clamd.conf', 'clamav', 'clamav', 0o644),
    ('file', '/etc/clamav/freshclam.conf', 'clamav', 'clamav', 0o644),
    (
        'file', '/etc/cron.d/update_clamav_virus_database', 'root', 'root',
        0o644
    ),
    ('file', '/etc/cron.d/run_clamav_scan', 'root', 'root', 0o644),
    ('file', '/etc/logrotate.d/clamav-cron-jobs', 'root', 'root', 0o644),
    ('file', '/etc/logrotate.d/clamav-daemon', 'root', 'root', 0o644),
    ('file', '/etc/logrotate.d/clamav-freshclam', 'root', 'root', 0o644),
    ('directory', '/var/lib/clamav', 'clamav', 'clamav', 0o755),
])
def test_files_and_folders(host, path_type, path, user, group, mode):
    """
    Ensure needed folders exists
    """

    current_path = host.file(path)

    assert current_path.exists
    assert current_path.user == user
    assert current_path.group == group
    assert current_path.mode == mode

    if path_type == 'directory':
        assert current_path.is_directory
    elif path_type == 'file':
        assert current_path.is_file
    elif path_type == 'symlink':
        assert current_path.is_symlink
