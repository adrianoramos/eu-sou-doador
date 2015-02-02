Eu Sou Doador
==============

Serviço para ajudar pessoas que precisam de doação de sangue a encontrar doadores compatíveis mais próximos.

Requisitos do ambiente de desenvolvimento
-----------------------------------------

* Python 2.7
* Postgres 9.1
* GEOS
* PROJ.4
* GDAL
* PostGIS
* RabbitMQ

Você pode obter ajuda sobre a instalação do GEOS, PROJ, GDAL e PostGIS em: https://docs.djangoproject.com/en/1.6/ref/contrib/gis/install/geolibs/

Requisitos do ambiente Python
-----------------------------

* django
* bpython
* django-braces
* django-model-utils
* logutils
* south
* psycopg2
* celery
* django-autoslug
* django-widget-tweaks
* django-contact-form
* coverage
* django-discover-runner
* django-debug-toolbar
* sphinx

Instalação das dependências
---------------------------

    $ pip install -r requirements.txt

Rodando a aplicação localmente
------------------------------

    $ python manage.py runserver

Se você está usando Vagrant.

    $ python manage.py runserver [::]:8000

ou simplesmente executar o arquivo local.sh usando o seguinte comando:

    $ sh local.sh

O Site
--------

O exemplo mais atual e funcional está em http://eusoudoador.com.br
