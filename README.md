# clamav

[![Build Status](https://travis-ci.org/Temelio/ansible-role-clamav.svg?branch=master)](https://travis-ci.org/Temelio/ansible-role-clamav)

Install clamav package.

## Requirements

This role requires Ansible 2.0 or higher,
and platform requirements are listed in the metadata file.

## Testing

This role contains two tests methods :
- locally using Vagrant
- automatically with Travis

### Testing dependencies
- install [Vagrant](https://www.vagrantup.com)
- install [Vagrant serverspec plugin](https://github.com/jvoorhis/vagrant-serverspec)
    $ vagrant plugin install vagrant-serverspec
- install [Vagrant triggers plugin](https://github.com/emyl/vagrant-triggers)
    $ vagrant plugin install vagrant-triggers
- install ruby dependencies
    $ bundle install

### Running tests

#### Run playbook and test

- if Vagrant box not running
    $ vagrant up

- if Vagrant box running
    $ vagrant provision

## Role Variables

### Default role variables

    # Can be used to overwrite os role values
    clamav_packages: []

    # General settings
    clamav_log_folder: '/var/log/clamav'
    clamav_config_folder: '/etc/clamav'
    clamav_config_owner: 'clamav'
    clamav_config_group: 'clamav'
    clamav_config_mode: '0644'

    clamav_clamd_binary: '/usr/sbin/clamd'
    clamav_freshclam_binary: '/usr/bin/freshclam'
    clamav_clamd_service_name: 'clamav-daemon'
    clamav_freshclam_service_name: 'clamav-freshclam'
    clamav_scan_binary: '/usr/sbin/clamscan'

    # Virus database update cron job
    clamav_cron_update_create_task: True
    clamav_cron_update_minute: 2
    clamav_cron_update_hour: 15
    clamav_cron_update_weekday: '*'
    clamav_cron_update_day: '*'
    clamav_cron_update_month: '*'

    # Scan cron job
    clamav_cron_scan_create_task: True
    clamav_cron_scan_minute: 2
    clamav_cron_scan_hour: 30
    clamav_cron_scan_weekday: '*'
    clamav_cron_scan_day: '*'
    clamav_cron_scan_month: '*'
    clamav_cron_scan_dest:
      - '/data'
      - '/tmp'
    clamav_cron_scan_exclude_dirs: []

    # Logrotate configuration
    clamav_logrotate_config:
      - filename: '/etc/logrotate.d/clamav-daemon'
        log_pattern: '/var/log/clamav/clamav.log'
        options:
          - 'rotate 12'
          - 'weekly'
          - 'compress'
          - 'delaycompress'
          - 'create 640 clamav adm'
          - 'postrotate'
          - '/etc/init.d/clamav-daemon reload-log > /dev/null'
          - 'endscript'
      - filename: '/etc/logrotate.d/clamav-freshclam'
        log_pattern: '/var/log/clamav/freshclam.log'
        options:
          - 'rotate 12'
          - 'weekly'
          - 'compress'
          - 'delaycompress'
          - 'missingok'
          - 'create 640 clamav adm'
          - 'postrotate'
          - '/etc/init.d/clamav-freshclam reload-log > /dev/null'
          - 'endscript'
      - filename: '/etc/logrotate.d/clamav-cron-jobs'
        log_pattern: '/var/log/clamav/cron*.log'
        options:
          - 'rotate 7'
          - 'daily'
          - 'compress'
          - 'delaycompress'
          - 'missingok'
          - 'create 640 clamav adm'

    # Clamd config file variables
    clamav_clamd_local_socket: '/var/run/clamav/clamd.ctl'
    clamav_clamd_fix_stale_socket: 'true'
    clamav_clamd_local_socket_group: 'clamav'
    clamav_clamd_local_socket_mode: 666
    clamav_clamd_user: 'clamav'
    clamav_clamd_allow_supplementary_groups: 'true'
    clamav_clamd_scan_mail: 'true'
    clamav_clamd_scan_archive: 'true'
    clamav_clamd_archive_block_encrypted: 'false'
    clamav_clamd_max_directory_recursion: 15
    clamav_clamd_follow_directory_symlinks: 'false'
    clamav_clamd_follow_file_symlinks: 'false'
    clamav_clamd_read_timeout: 180
    clamav_clamd_max_threads: 12
    clamav_clamd_max_connection_queue_length: 15
    clamav_clamd_log_syslog: 'false'
    clamav_clamd_log_rotate: 'true'
    clamav_clamd_log_facility: 'LOG_LOCAL6'
    clamav_clamd_log_clean: 'false'
    clamav_clamd_log_verbose: 'false'
    clamav_clamd_pid_file: '/var/run/clamav/clamd.pid'
    clamav_clamd_database_directory: '/var/lib/clamav'
    clamav_clamd_self_check: 3600
    clamav_clamd_foreground: 'false'
    clamav_clamd_debug: 'false'
    clamav_clamd_scan_pe: 'true'
    clamav_clamd_max_embedded_pe: '10M'
    clamav_clamd_scan_ole2: 'true'
    clamav_clamd_scan_pdf: 'true'
    clamav_clamd_scan_html: 'true'
    clamav_clamd_max_html_normalize: '10M'
    clamav_clamd_max_html_no_tags: '2M'
    clamav_clamd_max_script_normalize: '5M'
    clamav_clamd_max_zip_type_rcg: '1M'
    clamav_clamd_scan_swf: 'true'
    clamav_clamd_detect_broken_executables: 'false'
    clamav_clamd_exit_on_oom: 'false'
    clamav_clamd_leave_temporary_files: 'false'
    clamav_clamd_algorithmic_detection: 'true'
    clamav_clamd_scan_elf: 'true'
    clamav_clamd_idle_timeout: 30
    clamav_clamd_phishing_signatures: 'true'
    clamav_clamd_phishing_scan_urls: 'true'
    clamav_clamd_phishing_always_block_ssl_mismatch: 'false'
    clamav_clamd_phishing_always_block_cloak: 'false'
    clamav_clamd_partition_intersection: 'false'
    clamav_clamd_detect_pua: 'false'
    clamav_clamd_scan_partial_messages: 'false'
    clamav_clamd_heuristic_scan_precedence: 'false'
    clamav_clamd_structured_data_detection: 'false'
    clamav_clamd_command_read_timeout: 5
    clamav_clamd_send_buf_timeout: 200
    clamav_clamd_max_queue: 100
    clamav_clamd_extended_detection_info: 'true'
    clamav_clamd_ole2_block_macros: 'false'
    clamav_clamd_scan_on_access: 'false'
    clamav_clamd_allow_all_match_scan: 'true'
    clamav_clamd_force_to_disk: 'false'
    clamav_clamd_disable_cert_check: 'false'
    clamav_clamd_disable_cache: 'false'
    clamav_clamd_max_scan_size: '100M'
    clamav_clamd_max_file_size: '25M'
    clamav_clamd_max_recursion: 10
    clamav_clamd_max_files: 10000
    clamav_clamd_max_partitions: 50
    clamav_clamd_max_icons_pe: 100
    clamav_clamd_stats_enabled: 'false'
    clamav_clamd_stats_pe_disabled: 'true'
    clamav_clamd_stats_host_id: 'auto'
    clamav_clamd_stats_timeout: 10
    clamav_clamd_stream_max_length: '25M'
    clamav_clamd_log_file: "{{ clamav_log_folder }}/clamav.log"
    clamav_clamd_log_time: 'true'
    clamav_clamd_log_file_unlock: 'false'
    clamav_clamd_log_file_max_size: 0
    clamav_clamd_bytecode: 'true'
    clamav_clamd_bytecode_security: 'TrustSigned'
    clamav_clamd_bytecode_timeout: 60000
    clamav_clamd_official_database_only: 'false'
    clamav_clamd_cross_filesystems: 'true'

    # Fresclam config file variables
    clamav_freshclam_database_owner: 'clamav'
    clamav_freshclam_update_log_file: "{{ clamav_log_folder }}/freshclam.log"
    clamav_freshclam_log_verbose: 'false'
    clamav_freshclam_log_syslog: 'false'
    clamav_freshclam_log_facility: 'LOG_LOCAL6'
    clamav_freshclam_log_file_max_size: 0
    clamav_freshclam_log_rotate: 'true'
    clamav_freshclam_log_time: 'true'
    clamav_freshclam_foreground: 'false'
    clamav_freshclam_debug: 'false'
    clamav_freshclam_max_attempts: 5
    clamav_freshclam_database_directory: '/var/lib/clamav'
    clamav_freshclam_dns_database_info: 'current.cvd.clamav.net'
    clamav_freshclam_allow_supplementary_groups: 'false'
    clamav_freshclam_pid_file: '/var/run/clamav/freshclam.pid'
    clamav_freshclam_connect_timeout: 30
    clamav_freshclam_receive_timeout: 30
    clamav_freshclam_test_databases: 'yes'
    clamav_freshclam_scripted_updates: 'yes'
    clamav_freshclam_compress_local_database: 'no'
    clamav_freshclam_bytecode: 'true'
    clamav_freshclam_checks: 24
    clamav_freshclam_database_mirror:
      - 'database.clamav.net'
      - 'db.local.clamav.net'

## Dependencies

None

## Example Playbook

    - hosts: servers
      roles:
         - { role: Temelio.clamav }

## License

MIT

## Author Information

Alexandre Chaussier (for Temelio company)
- http://temelio.com
- alexandre.chaussier [at] temelio.com
