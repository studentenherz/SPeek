#! /bin/bash

while true; do
		read -p "Are you sure you want to uninstall (y/N)? " yn
		[[ $yn == '' ]] && yn='N'
		case $yn in
				[Yy]* ) break;;
				[Nn]* ) exit;;
				* ) echo "Please answer yes or no.";;
		esac
done

echo "Uninstalling..."

# nginx 
sudo rm /etc/nginx/sites-enabled/speek.panel
sudo rm /etc/nginx/sites-available/speek.panel

sudo systemctl restart nginx

# speek service
sudo systemctl stop speek
sudo rm /etc/systemd/system/speek.service

# env congif
sudo rm /etc/sysconfig/speek.env

# other files
rm speek.panel speek.service
rm -r venv
rm speek/database.db

echo -e "Done!\n To also remove this folder run\nspeek_dir=$(pwd) && cd .. && rm -r $speek_dir"
