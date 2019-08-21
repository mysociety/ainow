if ! grep -q "cd /vagrant" ~/.bashrc ; then 
    echo "cd /vagrant/ainow" >> ~/.bashrc 
fi 