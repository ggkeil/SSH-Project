# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 18:50:25 2019

@author: eagle
"""
import paramiko
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import ssh_conf
import socket

class SSH:
    "Class to connect to remote server"
    
    def __init__(self, Host, User, Password, Timeout):
        self.ssh_output = None
        self.ssh_error = None
        self.client = None
        self. host = Host
        self.username = User
        self.password = Password
        self.timeout = float(Timeout)
        
    def connect(self):
        "Login to the remote server"
        try:
            # Paramiko.SSHClient can be used to make connections to the remote server and transfer files
            print("Establishing SSH connection")
            self.client = paramiko.SSHClient()
            
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # connect to the server
            if self.password == '':
                self.pkey = paramiko.RSAKey.from_private_key_file(self.pkey)
                self.client.connect(hostname=self.host, port=self.port, username=self.username,pkey=self.pkey ,timeout=self.timeout, allow_agent=False, look_for_keys=False)
                print("Connected to the server " + str(self.host))
            else:
                self.client.connect(hostname=self.host, port=self.port, username=self.username, password=self.password, timeout=self.timeout, allow_agent=False, look_for_keys=False)
                print("Connected to the server " + str(self.host))
        except paramiko.AuthenticationException:
            print("Authentication failed, please verify your credentials")
            result_flag = False
        except paramiko.SSHException as sshException:
            print("Could not establish SSH connection: %s" % sshException)
            result_flag = False
        except socket.timeout as e:
            print("Connection timed out")
            result_flag = False
        except Exception as e:
            print('\nException in connecting to the server')
            print('PYTHON SAYS:' + e)
            result_flag = False
            self.client.close()
        else:
            result_flag = True
            
        return result_flag
    
    def execute_command(self, commands):
        """Execute a command on the remote host.Return a tuple containing
        an integer status and two strings, the first containing stdout
        and the second containing stderr from the command."""
        
        self.ssh_output = None
        result_flag = True
        try:
            if self.connect():
                for command in commands:
                    print("Executing command --> {}".format(command))
                    
        