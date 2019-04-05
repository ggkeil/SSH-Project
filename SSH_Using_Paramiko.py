# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 18:50:25 2019

@author: eagle
"""
import paramiko
import os
import sys
import time
import getpass

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import socket

class SSH:
    "Class to connect to remote server"
    
    def __init__(self, Host, User, Password, Timeout, Port):
        self.ssh_output = None
        self.ssh_error = None
        self.client = None
        self. host = Host
        self.username = User
        self.password = Password
        self.timeout = float(Timeout)
        self.port = Port
        
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
                print("Connected to the server ", self.host)
            else:
                self.client.connect(hostname=self.host, port=self.port, username=self.username, password=self.password, timeout=self.timeout, allow_agent=False, look_for_keys=False)
                print("Connected to the server ", self.host)
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
            print('PYTHON SAYS:', e)
            result_flag = False
            self.client.close()
        else:
            result_flag = True
            
        return result_flag
    
    def execute_command(self, command):
        """Execute a command on the remote host.Return a tuple containing
        an integer status and two strings, the first containing stdout
        and the second containing stderr from the command."""
        
        self.ssh_output = None
        result_flag = True
        try:
            if self.connect():
                print("Executing command --> {}".format(command))
                stdin, stdout, stderr = self.client.exec_command(command, timeout = 10)
                self.ssh_output = stdout.read()
                self.ssh_error = stderr.read()
                if self.ssh_error:
                    print("Problem occurred while running command: " + command + ". The error is " + self.ssh_error)
                    result_flag = False
                else:
                    print("Command execution completed successfully", command)
                    print(str(self.ssh_output)) # print the result of executing the command
                
                self.client.close()
                
            else:
                print("Could not establish SSH connection")
                result_flag = False
        
        except socket.timeout as e:
            print("Command timed out.", command)
            self.client.close()
            result_flag = False
        except paramiko.SSHException:
            print("Failed to execute the command!", command)
            self.client.close()
            result_flag = False
            
        return result_flag
    
    def upload_file(self, uploadlocalfilepath, uploadremotefilepath):
        "This method uploads the file to remote server"
        result_flag = True
        try:
            if self.connect():
                ftp_client = self.client.open_sftp()
                ftp_client.put(uploadlocalfilepath, uploadremotefilepath)
                ftp_client.close()
                self.client.close()
            else:
                print("Could not establish SSH connection")
                result_flag = False
        except Exception as e:
            print('\nUnable to upload the file to the remote server', uploadremotefilepath)
            print('PYTHON SAYS:', e)
            result_flag = False
            ftp_client.close()
            self.client.close()
            
        return result_flag
    
    def download_file(self, downloadremotefilepath, downloadlocalfilepath):
        "This method downloads the file from the remote server"
        result_flag = True
        try:
            if self.connect():
                ftp_client = self.client.open_sftp()
                ftp_client.get(downloadremotefilepath, downloadlocalfilepath)
                ftp_client.close()
                self.client.close()
            else:
                print("Could not establish SSH connection")
                result_flag = False
        except Exception as e:
            print('\nUnable to download the file from the remote server', downloadremotefilepath)
            print('PYTHON SAYS:', e)
            result_flag = False
            ftp_client.close()
            self.client.close()
        
        return result_flag

host = input("Enter host name: ")
port = input("Port: ")
user = input("login as: ")
password = getpass.getpass(prompt = user + "@" + host + "'s password: ") # only supported when executing in command prompt

ssh_obj = SSH(str(host), str(user), str(password), 20, int(port))
ssh_obj.connect()
command = input("Enter a command: ")
ssh_obj.execute_command(command)