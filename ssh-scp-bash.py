import os
import paramiko
from scp import SCPClient

print('Please enter csd release (example: 00348-6): ')
release = input()
# release = "/tmp"

web_files_dir = '/mnt/c/Users/r.nagmetov/Desktop/New folder'
app_files_dir = '/mnt/c/Users/r.nagmetov/Desktop/New folder'
api_files_dir = '/mnt/c/Users/r.nagmetov/Desktop/New folder'
iss_files_dir = '/mnt/c/Users/r.nagmetov/Desktop/New folder'

web_sshkey = "/mnt/c/cred/ssh/TEST/csd_ec2-user.pem"
iss_sshkey = "/mnt/c/cred/ssh/TEST/csd_ec2-user.pem"

web_files = [f'common-bin-R{release}-aix.tar.gz',  \
                f'settle-gui-common-R{release}-aix.tar.gz', \
                f'settle-gui-R{release}-aix.tar.gz', \
                f'tools-bin-R{release}-aix.tar.gz']


web_commands = f'''sudo -i
/opt/avenir/common-bin/sbin/systems stop
cd /tmp/
tar xvf /tmp/tools-bin-R{release}-aix.tar.gz -C /tmp
cd tools-bin/
./install.sh
cd ../
rm -rf tools-bin/
cd /opt/avenir/tools-bin/bin/
./runtask repair
./runtask os-packages
'''

inter_comm = '''y
y
y
'''


def copy_ssh(rsakey_dir, host, user, files_to_copy, files_dir, commands, int_comm):
    k = paramiko.RSAKey.from_private_key_file(rsakey_dir)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("Connecting to csd-web ...")
    c.connect(hostname = host, username = user, pkey = k)
    print("Connected!")

    for i in files_to_copy:
        with SCPClient(c.get_transport()) as scp:
            print('Copy', i, '---> ', end='')
            scp.put(f'{files_dir}/{i}', f'/tmp/{i}')
            print('Done')

    print('Сopying has been done successfully!', '================================', ' ', sep='\n')

    channel = c.invoke_shell()
    stdin = channel.makefile('wb')
    stdout = channel.makefile('rb')
    
    print('===== Executing commands =====')
    stdin, stdout, stderr = c.exec_command(commands)
    stdin.write(int_comm)
    print(stdout.read().decode())
    print(stderr.read().decode())
    stdout.close()
    stdin.close()
    stderr.close()
    c.close()


copy_ssh(web_sshkey, "192.168.1.70", "root", web_files, web_files_dir, web_commands, inter_comm)
