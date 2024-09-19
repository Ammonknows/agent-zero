#!/bin/bash

# Ensure .bashrc is in the root directory
if [ ! -f /root/.bashrc ]; then
    cp /etc/skel/.bashrc /root/.bashrc
    chmod 777 /root/.bashrc
fi

# Ensure .profile is in the root directory
if [ ! -f /root/.profile ]; then
    cp /etc/skel/.profile /root/.profile
    chmod 777 /root/.profile
fi

# Start SSH service
exec /usr/sbin/sshd -D
