# theezy-trader-core-platform
The Theezy Trader platform is a collection of DigitalOcean functions that powers the Backend infrastructure of the Theezy Trader application

## Getting Started
This project uses out-of-the-box DigitalOcean functions configuration project structure with a [project.yml](https://docs.digitalocean.com/products/functions/reference/project-configuration/) file at the root of the project. 
* The DigitalOcean documentation on creating functions can be found [here](https://docs.digitalocean.com/products/functions/how-to/create-functions/)

## Build Process
This project is split up into two layers of function groups outlined by python packages. The digitalocean functions layer and the common lib layer.
The lib common layer holds the instructions for building each function and including common functionality as well as installing external dependencies.
The `build.sh` script is used to ensure the modules within `requirements.txt` file is installed into each function and that the common lib package exists
within each function at runtime. This occurs by copying the lib folder into each function during that function's build execution phase.

_Note: Each new function package introduced to the project must be added to the build.sh script to ensure the lib folder to that function._  
The DigitalOcean functions build process documentation can be found [here](https://docs.digitalocean.com/products/functions/reference/build-process/)