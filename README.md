Installation
============

You need to install requests:

pip install requests

Configuration
=============

You need to declare the 2 following environments variables :

    - GOOGLE_KEY : Your googlemap API key

    - OSM_URL : The url to your nominatim server (default is http://localhost/nominatim/search.php)


Example
=======

    ./geocoding.py -g OSM -g Google -t City -o sample_out.csv sample_in.csv 
