#!/usr/bin/python3
import paramiko
import os

private_key_path = '/home/sel/.ssh/school'
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
ssh_client.connect('3.90.70.66', username='ubuntu', pkey=private_key)
stdin, stdout, stderr = ssh_client.exec_command('ls')
print(stdout.read().decode())
ssh_client.close()
