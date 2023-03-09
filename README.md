# CyberSleuth
Carleton College Computer Science Capstone Project.
Profiling and Identifying Websites Through Packet Tracing Analysis.
Developed by Aiden Chang, Luke Major, Shaun Baron-Furuyama, Jeylan Jones, and Anders Shenholm
Check out our [Website](https://cs.carleton.edu/cs_comps/2223/csiOlin/final-results/) and [Presentation Slides](https://docs.google.com/presentation/d/1U0ZS9FJ87KXPLVZnWpzN3VO7B7C6Hcd8K937XkT7x4Y/edit#slide=id.g1f48a6d175f_0_0)!

Table of contents
=================

<!--ts-->
* [Installation and Running the Code](#installation-and-running-the-code)
* [About the Code](#about-the-code)
* [User Workflow](#user-workflow)
    * [Closing all tabs](#closing-all-tabs)
    * [Profiling Background](#profiling-background)
    * [Profiling a Website](#profiling-a-website)
    * [Uploading your own trace](#uploading-your-own-trace)
    * [View your built profiles](#view-your-built-profiles)
<!--te-->


Installation and Running the Code
============


Clone the github repository, install and activate python venv. 

Install a python virtual environment:
```
python3 -m venv [path to virtual environment]
```

To start virtual environment and install required packages:
```
cd [path to virtual environment]
source bin/activate
pip install -r requirements.txt
```

To launch the GUI, type:
```
python3 interface.py
```

About the Code
============
This project was part of a capstone project of Carleton College's Computer Science department.
This code was developed by Aiden Chang, Luke Major, Shaun Baron-Furuyama, Jeylan Jones, and Anders Shenholm. Please visit our [website](https://cs.carleton.edu/cs_comps/2223/csiOlin/final-results/) and [Presentation Slides](https://docs.google.com/presentation/d/1U0ZS9FJ87KXPLVZnWpzN3VO7B7C6Hcd8K937XkT7x4Y/edit#slide=id.g1f48a6d175f_0_0) for more details! 

User Workflow
============
All the details of each userworkflow is included in our [website](https://cs.carleton.edu/cs_comps/2223/csiOlin/final-results/) and [Presentation Slides](https://docs.google.com/presentation/d/1U0ZS9FJ87KXPLVZnWpzN3VO7B7C6Hcd8K937XkT7x4Y/edit#slide=id.g1f48a6d175f_0_0).
### Closing all tabs
After launching the GUI, the first thing the user should do is read the instructions.
The instructions will instruct you to shut down all processes excluding the GUI running on your device (this includes background processes like bluetooth and vpn).  

### Profiling Background
The first thing the user should do after is to profile their background. When we are profiling applications, we build a profile by monitoring the ip addresses we detect on the users computer. To create an accurate background profile, we need the traces to be as clean as possible. 

The user can choose the timeout by typing it in the white box (the default is 600). The user will not be able to access any other workflow before they have a background profile. This process should take around 10 minutes. 

### Profiling a Website
Once the background Profile is made, the user can profile a website. Simply type in the website name (ex: https://www.open.spotify.com) and the program should start profiling the website. Once done, the program will save a profile of the website in your ```/ip_profiles``` folder. It will also build a graph in the `/bar_charts` folder.

### Uploading your own trace
You can upload your own noisy trace to compare it to the built profiles. The uploaded trace must be a .pcap file. After hitting the 'generate profile' button, the program will generate a text file report in the directory of this code as `full_report.txt`. The code will also generate graph reports in `/match_graphs`. 

### View your built profiles
You can access the built profiles on the "check_built_profiles" button. Double clicking a built profile generates a graph on the built profile. 
> **Note**
> Due to the way we profile, a user will not be able to profile "background" and "chrome"



