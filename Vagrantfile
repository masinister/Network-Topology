# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.

Vagrant.configure(2) do |config|

  # 64 bit Ubuntu Vagrant Box
  config.vm.box = "ubuntu/trusty64"

  ## Configure hostname and port forwarding
  config.vm.hostname = "cs513"
  config.ssh.forward_x11 = true
  # For jupyter notebook server
  config.vm.network "forwarded_port", guest: 8888, host: 8888
  # For HTTP proxy
  config.vm.network "forwarded_port", guest: 12000, host: 12000

  vagrant_root = File.dirname(__FILE__)

  ## Provisioning
  config.vm.provision "shell", inline: <<-SHELL
     # Assignment 1
     sudo apt-get update
     sudo apt-get -y upgrade
     # Build Python 2.7.12 from source
     sudo apt-get install -y libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev zlib1g-dev
     sudo wget https://www.python.org/ftp/python/3.8.3/Python-3.8.3.tgz

     sudo tar xzf Python-3.8.3.tgz
     cd Python-3.8.3
     sudo ./configure --enable-optimizations
     sudo make altinstall

     sudo apt-get install -y libssl-dev curl python3-pip

     # Set correct permissions for bash scripts
     find /vagrant -name "*.sh" | xargs chmod -v 744

     # If the repository was pulled from Windows, convert line breaks to Unix-style
     sudo apt-get install -y dos2unix
     printf "Using dos2unix to convert files to Unix format if necessary..."
     find /vagrant -name "*" -type f | xargs dos2unix -q

     # Install Python packages
     sudo pip install mininet
     sudo pip install nbconvert
     sudo pip install numpy
     sudo pip install matplotlib
     sudo apt-get install -y mininet
     sudo apt-get install -y python-numpy
     sudo apt-get install -y python-matplotlib
     sudo apt-get install -y whois
     sudo pip install ipaddress

     # Start in /vagrant instead of /home/vagrant
     if ! grep -Fxq "cd /vagrant" /home/vagrant/.bashrc
     then
      echo "cd /vagrant" >> /home/vagrant/.bashrc
     fi
  SHELL

  ## Provisioning to do on each "vagrant up"
  config.vm.provision "shell", run: "always", inline: <<-SHELL
    sudo tzupdate 2> /dev/null
    # Assignment 2
    sudo modprobe tcp_probe port=5001 full=1
  SHELL

  ## CPU & RAM
  config.vm.provider "virtualbox" do |vb|
    vb.customize ["modifyvm", :id, "--cpuexecutioncap", "100"]
    vb.memory = 2048
    vb.cpus = 1
  end

end
