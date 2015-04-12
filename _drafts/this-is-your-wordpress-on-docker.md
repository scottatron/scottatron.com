[Install Fig](http://www.fig.sh/install.html)

    sudo pip install fig --upgrade

[Getting started with Fig and Wordpress](http://www.fig.sh/wordpress.html)

Install Composer by adding

    RUN DEBIAN_FRONTEND=noninteractive apt-get install php5-json curl -y
    RUN curl -sS https://getcomposer.org/installer | php 
    RUN mv composer.phar /usr/local/bin/composer

to the Dockerfile and running `fig build web`

Add a composer.json that contains wp-cli as a development dependency:

    {
      "require-dev": {
        "wp-cli/wp-cli": "~0.17.0"
      }
    }

and install it:

    fig run web bash
    cd /code
    composer install

Add bin/wp:

    #!/usr/bin/env bash
    vendor/bin/wp --allow-root "$@"

and make sure it's `chmod +x`. This silences the root warning from wp-cli

Install Wordpress site:
    
    fig run web bash
    cd /code
    bin/wp core install --url='http://www.lucyandthepowderroom.com:8000/' --title='Lucy and the Powder Room' --admin_user='Scott Arthur' --admin_password='QpJeZLHEvKZZttbJCM26' --admin_email='scott@scottatron.com'

Note the inclusion of port 8000 in the url. This is needed for the development env. This can be changed with:

    bin/wp option update siteurl http://www.lucyandthepowderroom.com:8000/
    bin/wp option update home http://www.lucyandthepowderroom.com:8000/

Fig up!

    fig up

