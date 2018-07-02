# PlanetaryGeologicMappers

[![Join the chat at https://gitter.im/USGS-Astrogeology/PlanetaryGeologicMappers](https://badges.gitter.im/USGS-Astrogeology/PlanetaryGeologicMappers.svg)](https://gitter.im/USGS-Astrogeology/PlanetaryGeologicMappers?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

The web site for the planetary geologic mappers (PGM).  The website includes static content
with resources for mappers and current status of mapping projects including GIS footprints.

This project is the conversion of the website to use Python/Flask as the web application container.

By default, the commands in the following section must be run as root, so they use 'sudo.'  Commands on Windows are the same except that the user may omit 'sudo.'

## 1. Install Docker

To install Docker, simply follow the [installation instructions](https://docs.docker.com/install/)for your system.

## 2. Install Docker-Compose

Though some distributions of Docker (mostly on Windows and OSX) are shipped with docker-compose, it may be necessary for some users to perform a separate installation.  To determine if you need to perform this installation, open a terminal and type:

    > sudo docker-compose
    
If the command outputs usage instructions, then you may skip this step.  If, instead, the output reads "command not found," then follow the installation instructions [here](https://docs.docker.com/compose/install/).

## 3. Building the Docker container

To build the Docker container, navigate (within a terminal) to the top level of the PGM directory and use the following command:

    > sudo docker-compose build
    
## 4. Starting the service

To start the service, use the following command:

    > sudo docker-compose up