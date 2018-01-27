# security
## As system that uses multiple camera's as a motion sensor
#### The purpose of this project is create a motion sensor security system out of normal webcams.

#### Required custom Python packages
1. [observer](https://github.com/mkhabelaj/observer)
1. [Camera](https://github.com/mkhabelaj/camera)
1. [randgen](https://github.com/mkhabelaj/randgen)
1. [imagestream](https://github.com/mkhabelaj/imagestream)

#### Other Requirements
1. Openvc
1. Screen (terminal utility)
1. Postgres sql (version 9.4 and up)
1. virtualenv

#### Things to consider
I built this project using:
  1. This project runs hand to hand with this project [security_site](https://github.com/mkhabelaj/security_site)
    1. This project is the backend, and [security_site](https://github.com/mkhabelaj/security_site) is the frontend where the camera stream is displayed
  1. Python 3.4 
  1. Ubuntu 14.04
  
#### Usage

1. Create a virtual environment named security
1. Initiate virtual enrolment ```workon security```
1. ``` cd ``` into the project and run the following command 
    1. ```Python
         python security.py
        ``` 
1. The above command will detect the number of cameras available and start an image stream to randomly generated ports
1. Run the following project to see the camera streams [security_site](https://github.com/mkhabelaj/security_site)




