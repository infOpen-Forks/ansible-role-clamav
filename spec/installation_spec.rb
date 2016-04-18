require 'serverspec'

if ENV['TRAVIS']
    set :backend, :exec
end

describe 'clamav Ansible role' do

    # Declare variables
    packages = Array[]
    clamav_user = ''
    clamav_home = ''
    clamd_process_name = ''
    freshclam_process_name = ''
    clamd_service_name = ''
    freshclam_service_name = ''
    clamd_config_file = ''
    freshclam_config_file = ''
    clamav_config_mode = 600

    if ['debian', 'ubuntu'].include?(os[:family])
        packages = Array[ 'clamav', 'clamav-base', 'clamav-daemon' ]
        clamav_user = 'clamav'
        clamav_group = 'clamav'
        clamav_home = '/var/lib/clamav'
        clamd_process_name = 'clamd'
        freshclam_process_name = 'freshclam'
        clamd_service_name = 'clamav-daemon'
        freshclam_service_name = 'clamav-freshclam'
        clamd_config_file = '/etc/clamav/clamd.conf'
        freshclam_config_file = '/etc/clamav/freshclam.conf'
    end

    it 'install role packages' do
        packages.each do |pkg_name|
            expect(package(pkg_name)).to be_installed
        end
    end

    describe user(clamav_user) do
        it { should exist }
        it { should have_login_shell('/bin/false') }
        it { should belong_to_group(clamav_group) }
        it { should have_home_directory(clamav_home) }
    end

    describe process(clamd_process_name) do
        it { should be_running }
        its(:user) { should eq clamav_user }
    end

    describe process(freshclam_process_name) do
        it { should be_running }
        its(:user) { should eq clamav_user }
    end

    describe service(clamd_service_name) do
        it { should be_running }
        it { should be_enabled }
    end

    describe service(freshclam_service_name) do
        it { should be_running }
        it { should be_enabled }
    end

    describe file(clamd_config_file) do
        it { should exist }
        it { should be_file }
        it { should be_owned_by(clamav_user) }
        it { should be_grouped_into(clamav_group) }
        it { should be_mode(clamav_config_mode) }
    end

    describe file(freshclam_config_file) do
        it { should exist }
        it { should be_file }
        it { should be_owned_by(clamav_user) }
        it { should be_grouped_into(clamav_group) }
        it { should be_mode(clamav_config_mode) }
    end
end

