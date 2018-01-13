
### How to install python 3.6 in Ubuntu
* https://stackoverflow.com/questions/42558133/upgrading-python3-4-to-python3-6-on-ubuntu-breaks-pip

```
# Remove existing python 3.6 if installed with apt
$ sudo apt-get autoremove python3.6

# Get the source
$ wget https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tar.xz
$ tar xvf Python-3.6.1.tar.xz
$ cd Python-3.6.1

# Configure and install
$ sudo ./configure
$ sudo make altinstall

# Success!
$ pip3.6 -V
pip 9.0.1 from /usr/local/lib/python3.6/site-packages (python 3.6)

```


