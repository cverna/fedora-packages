#!/bin/bash -C
python /usr/share/fedoracommunity/setup.py develop
httpd -DFOREGROUD
echo "#########################################################
fedora-packages running on http://127.0.0.1:8080/packages
#########################################################"
tail -f /var/log/httpd/fedoracommunity_error_log
