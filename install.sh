#! /bin/bash

env='venv'
wdir=$(pwd)

echo "Step 1: Installing needed python dependencies."

# create python virtual-env
if [ ! -d "$env" ] 
then
	echo "Creating virtual environment at ${env}"
	virtualenv $env
fi

install requirements
source $env/bin/activate
echo "Installing required packages"
pip install -r requirements.txt

# create systemd service

echo "Step 2: Creating systemd service."

echo \
"[Unit]
Description = SPeek a simple web-based system monitor. 
After=network.target

[Service]
User=$(whoami)
Group=www-data
WorkingDirectory=${wdir}
Environment=\"PATH=${wdir}/env/bin\"
ExecStart=${wdir}/env/bin/gunicorn speek:app -b unix:speek.sock -m 007

[Install]
WantedBy=multi-user.target"  > speek.service

echo -e "================= speek.service ==================\n"
cat speek.service
echo -e "\n=============== end speek.service ================"

echo -e "Copying Unit file shown above into /etc/systemd/system/ for service setup"
sudo cp speek.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable speek
sudo systemctl restart speek


# configure nginx

echo "Step 3: Setting up Nginx configuration."

while true; do
    read -p "Would you like to set up a domain through Nginx (Y/n)? " yn
		[[ $yn == '' ]] && yn='Y'
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done
read -p "Please add the domain name you wich to set up for your SPeek: " domain


if [ ! -d '/etc/nginx' ]
then
	echo 'No Nginx detected in typical config path /etc/nginx, attempting to install with apt.'
	sudo apt install nginx
fi

nginx_site_file="speek.panel"

echo \
"server {
	listen 80;
	listen [::]:80;

	server_name ${domain};

	location / {
		include proxy_params;
		proxy_pass http://unix:${wdir}/speek.sock;
	}
}" > $nginx_site_file

[[ ! -d '/etc/nginx/sites-available' ]] && sudo mkdir /etc/nginx/sites-available
[[ ! -d '/etc/nginx/sites-enabled' ]] && sudo mkdir /etc/nginx/sites-enabled

sudo cp $nginx_site_file "/etc/nginx/sites-available/${nginx_site_file}"
[[ ! -e "/etc/nginx/sites-enabled/${nginx_site_file}" ]] && sudo ln -s "/etc/nginx/sites-available/${nginx_site_file}" "/etc/nginx/sites-enabled/${nginx_site_file}"

sudo systemctl restart nginx

echo -e "\nDone!\nSee speek service with: systemctl status speek\nSee nginx service with: systemctl status nginx"

echo -e "Step 4: SSL Certificate."

while true; do
    read -p "Would you like to set up a SSL certificate from Let's Encrypt (Y/n)? " yn
		[[ $yn == '' ]] && yn='Y'
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

if ! command -v certbot &> /dev/null
then
    echo "Certbot could not be found, installing with apt"
    sudo apt install certbot
fi

sudo certbot --nginx -n --redirect -d $domain