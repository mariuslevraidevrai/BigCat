# BigCat
# Description

BigCat is an opensource and secure messaging for local network like ncat.
- RSA to encrypt asymmetric fernet key
- Encrypt all message with fernet
- Hash password (SHA256) with hashlib
- No Logs

# Requirements

- Linux distro(Arch based, RHEL based or debian based)
- x86 CPU
- Python 3.12
- The rsa library (pip/pip3 install rsa)

# Installation

- Clone this repository
- execute bigcat.py(or compile manually the bigcat.py with pyinstaller)
- Enjoy

# Usage

- create : make a session on your device (Example : create 127.0.0.1 1234)
- join : connect to a session (Example : join 192.168.1.10 1234)
- clear : clear the console
- bye : quit bigcat

# Warning
Iam a beginner in dev and this is the first version of my project so there are probably many bugs thx :)
