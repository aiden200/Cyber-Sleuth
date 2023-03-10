# CyberSleuth
Carleton College Computer Science Capstone Project.
Profiling and Identifying Websites Through Packet Tracing Analysis.
Developed by Aiden Chang, Luke Major, Shaun Baron-Furuyama, Jeylan Jones, and Anders Shenholm
Check out our [Website](https://cs.carleton.edu/cs_comps/2223/csiOlin/final-results/) and [Presentation Slides](https://docs.google.com/presentation/d/1U0ZS9FJ87KXPLVZnWpzN3VO7B7C6Hcd8K937XkT7x4Y/edit#slide=id.g1f48a6d175f_0_0)!

<ins>Table of contents</ins>
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
* [Initial Approach](#initial-approach)
    * [Our Topic](#our-topic)
    * [Importance](#why-is-this-important-and-who-does-this-project-serve)
    * [Methodology](#methodology)
    * [Initial Deliverables](#initial-deliverables)
    * [App Profiles](#app-profiles)
    * [Strategy Documents](#strategy-documents)
    * [Machine Learning](#machine-learning)
<!--te-->


<ins>Installation and Running the Code</ins>
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
&emsp; This project was part of a capstone project of Carleton College's Computer Science department. Developed by Aiden Chang, Luke Major, Shaun Baron-Furuyama, Jeylan Jones, and Anders Shenholm. Please visit our [website](https://cs.carleton.edu/cs_comps/2223/csiOlin/final-results/) and [Presentation Slides](https://docs.google.com/presentation/d/1U0ZS9FJ87KXPLVZnWpzN3VO7B7C6Hcd8K937XkT7x4Y/edit#slide=id.g1f48a6d175f_0_0) for more details! 

User Workflow
============
All the details of each userworkflow is included in our [website](https://cs.carleton.edu/cs_comps/2223/csiOlin/final-results/) and [Presentation Slides](https://docs.google.com/presentation/d/1U0ZS9FJ87KXPLVZnWpzN3VO7B7C6Hcd8K937XkT7x4Y/edit#slide=id.g1f48a6d175f_0_0).
### Closing all tabs
&emsp; After launching the GUI, the first thing the user should do is read the instructions. The instructions will instruct you to shut down all processes excluding the GUI running on your device (this includes background processes like bluetooth and vpn).  

### Profiling Background
&emsp; The first thing the user should do after is to profile their background. When we are profiling applications, we build a profile by monitoring the ip addresses we detect on the users computer. To create an accurate background profile, we need the traces to be as clean as possible. 

&emsp; The user can choose the timeout by typing it in the white box (the default is 600). The user will not be able to access any other workflow before they have a background profile. This process should take around 10 minutes. 

### Profiling a Website
&emsp; Once the background Profile is made, the user can profile a website. Simply type in the website name (ex: https://www.open.spotify.com) and the program should start profiling the website. Once done, the program will save a profile of the website in your ```/ip_profiles``` folder. It will also build a graph in the `/bar_charts` folder.

### Uploading your own trace
&emsp; You can upload your own noisy trace to compare it to the built profiles. The uploaded trace must be a .pcap file. After hitting the 'generate profile' button, the program will generate a text file report in the directory of this code as `full_report.txt`. The code will also generate graph reports in `/match_graphs`. 

### View your built profiles
&emsp; You can access the built profiles on the "check_built_profiles" button. Double clicking a built profile generates a graph on the built profile. 
> **Note**
> Due to the way we profile, a user will not be able to profile "background" and "chrome"



Initial Approach
============

<details>
<summary>Expand</summary>

### Our Topic
&emsp; In the increasingly interconnected world we live in today, we take for granted our ability to log onto our favorite applications and instantly access data stored around the world. This paradigm has been the result of numerous decades of trial and error, with consistent efforts to improve computer capabilities and the common user experience. This process however, has obscured much of computers’ background tasks in favor of simple interfaces. So, how does this accessed data actually make its way to our machine? And in what ways do the applications on our machine communicate with the location that data is stored in? The answer to these questions varies by application, and examining the most popular ones will allow us to gain key insights into what kinds of intermediate exchanges are being used. 

### Why is this important, and who does this project serve?
&emsp; The implications of our project are not only relevant to computer scientists and those interested in networking, but to the daily lives of all technology users. Before the 21st century, this task would not seem daunting enough to warrant a large project in higher education, but this vast online system of communication has extended so widely and deeply in global society, that personal data can no longer be tracked so simply. Personal data is being sent to countless entities from connected devices in a persistent and rapid web of circulation, and this is for multiple reasons. Slicker and improved information access, as well as increased demand for new methods of long-distance communication are just two examples, but the most recent and momentous reason as of late has been the commodification of data. The general public is well aware of this, especially with headlines involving suspicious profits of companies such as Facebook and Twitter, yet a heavily technology-dependent world with little education on networks is left with no choice but to continue using their online services as normal, or if a user is more savvy, install a VPN on their devices. Knowing this, we will present the results of our project in a vocabulary and in a medium that common internet citizens can engage with, and we will use accurate language for well-informed computer scientists to relate to, so that we can educate everyone on how connections work, why they sometimes don’t, and we can encourage them to be mindful of their habits. 

### Our approach
&emsp; We will use personal and project-dedicated computers to collect and analyze data which details apps’ network interactions. Based on factors such as IP address, protocol, packet length, timing of when packets are sent, and port information, we will analyze packets using the open-source program Wireshark to build application profiles for some number of popular applications for our project. Additionally, we will produce a document detailing strategies and criteria affirming an ability to receive a trace and determine what applications are being used, thus allowing another person or group to repeat our process for profiled applications. Finally, if we have enough time after profiling popular applications, we will use machine learning algorithms to automate the process of distinguishing our profiled applications from other applications in a given packet trace.

### Methodology
&emsp; As mentioned in the background section, Wireshark will be the primary tool we use to analyze network traffic. We can use Wireshark to monitor incoming and outgoing data packets on personal and lab computers. Wireshark also gives us many tools for analyzing packets:
- Statistics menu - a range of data analysis including but not limited to:
    - all endpoints
    - all conversations
    - packet length average, histogram
    - rate of packets over time
- Display filters - limits observed packets to a selected subset based on:
    - protocol
    - ip address (source or destination)
    - packet size

&emsp; On top of the patterns we can find in Wireshark, we’ll also be using outside research to make our profiling more efficient. For example, if we can find detailed documentation for some app we want to profile, it could really help us know what to look for in that app’s network footprint. It’s also inevitable that we’ll want to look up the IP addresses that appear in our traces, for which we will need to do some online research. As these cases arise, we’ll carefully use outside sources.

&emsp; We will begin to decipher network traffic by focusing on a single app. We’ll collect traces that isolate that app’s activity, and study them in detail to piece together a profile of its network traffic. We will use the features provided by Wireshark, as well as other research as is needed. In this early stage of the project, we envision our application profiles to include information regarding commonly used IP addresses and ports, typical packet lengths (this won’t be used extensively, as we know that packet length can vary based on router), protocol information (QUIC vs. TCP vs. UDP etc.), and timing patterns. By “timing patterns”, we mean how frequently a given application communicates with the machine to which it is sending data. Some applications may send lots of packets in short “bursts” and then wait before sending another burst, while other applications may send fewer packets in a more consistent manner. Since so many moving parts are involved in a single trace, it would of course be difficult to find any one primary detail to indicate the journey of a packet, if not impossible. To find a method for narrowing down necessary steps for application profiling, we will naturally need to rely on a number of assumptions that can only come from sheer time and exposure to relationships between these details. Each of the applications we profile will likely have differing patterns upon closer inspection; we’ll compile these patterns into an outline of a profile.

&emsp; Once we have a working draft of a profile, we’ll look to identify that app in a packet trace containing many ‘conversations’ between many distinct applications running simultaneously. We can either take these traces ourselves or request them from our advisor for a stricter test of our profile. This will require us to carefully use our profiles to comb over these conversations in the packet trace, in order to decipher which applications are being run. In light of this, we may run into challenges in this process if there are applications that we haven’t profiled that look extremely similar in their traces to an application that we have profiled, or even if there are applications that we have profiled but resemble different ones when “background noise” from other applications interferes with our interpretation. We are expecting that the process of finding a profiled app in a busier trace will help us refine our profile and notice what really helps us identify an app’s network footprint in “the wild.” 

&emsp; As we become confident in our first profile, we can branch out into profiling other apps, using our sharpened skills and intuition to build and test new profiles. We’re imagining a tiered priority system to dictate which apps we focus on, where we only move on to the next tier after having strong profiles for all apps in the current tier. 

&emsp; We will develop strategy documents with each profile to describe a method for identifying apps based on their profile. It isn’t necessarily crucial that we have full strategy documents as soon as we have final drafts for each profile, but it could definitely be useful to have every researcher articulate the key pieces of the profile so that others less involved with that profile could pick it up quicker. This type of info can be written for a technical audience (us) as needed, so we wouldn’t really need final drafts for it to be useful. By the end of the project however, there should be no profile that doesn’t come with a polished strategy document. 

### Initial Deliverables
Minimum: 3 app profiles, each with a strategy document.

Maximum: 6+ app profiles, each with a strategy document. A program that automates app detection using our profiles and strategy documents.

### App Profiles
&emsp; Our app profiles consist of documents including any consistent characteristics of some app’s network traffic, including but not limited to: IP addresses, protocols, packet size, packet frequency, packet timing, port numbers, distinctive behaviors, and common errors. More basic information will be presented in a simple format used for all profiles, and more complicated patterns may be described in a general-purpose area for writing.

### Strategy Documents
&emsp; A strategy document corresponding to a given application profile will consist of formal instructions on how to pick out the application in a “noisy” or “messy” packet trace consisting of many different applications running at the same time. It will detail the method we used to profile the application and will include instructions on which IP addresses and ports to look at, what sort of byte flow would be expected in each direction, packet size, and packet timing (how frequently packets are sent in each direction) for our profiled application. Additionally, we will explain how we used the Statistics menu on wireshark to do this analysis and we will explain which graphs are the most helpful in picking the profiled application out from a messy trace. 

### Machine Learning
&emsp; As a final part of this project, we hope to translate the information from our strategy documents that detail how to pick given applications out from a “messy” trace into a machine learning algorithm (or set of algorithms) that automates this process. This would mean that we could give any trace to our algorithm and we would be able to see if any of our profiled applications are running. We will know by the end of this term whether we will be able to do this aspect of the project, and we will continue to explore ways in which we can gather traces “from the wild” to give to our algorithm. We are considering using a neural network to do this automation, but should a different type of machine learning approach work better we will pivot and go in another direction.

</details>








