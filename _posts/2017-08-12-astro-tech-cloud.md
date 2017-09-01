---
title: "Astronomical Techniques: Learning on the Cloud"
excerpt: "The cloud provides an enormous opportunity for decentralized, blended learning."
tags: 
  - post
  - teaching 
  - astronomy
  - cloud
last_modified_at: 2017-08-12T14:53:00
---

A few months ago, Russ Taylor and I wrote an [Op-Ed][oped] on the opportunities that Big Data
presents in Africa. This article focused on our findings within the South African context, and I
wrote about my experience with the African Research Cloud Astronomy Demonstrator ProjEct, **ARCADE**.

The teaching and learning intervention didn't really start off as a specific case-study for big
data, or data intensive computing, or cloud computing. Indeed, the project didn't even start off as
an _intervention_, since I was aiming to solve a simple problem -- teaching my class of 50 students
how to do a straightforward statistical analysis on radio and optical images.

The students were from a variety of different social and academic backgrounds. The engineers had
experience to digital signal processing, while the scientists had just started learning about
Fourier Series. Some of our students had their own laptops and plenty of experience with computers;
others were only just developing their expertise in computing. Throw into the mix the vagaries of
installing astronomical software. 
Thus, the challenge was to provide the students with comprehensive, persistent access to software
tools and data required for the project. 

I had three options opened to me:
    * Have the students install the software on their own computers.
        * This was a non-starter, since it would've taken longer for us to troubleshoot installation
          problems than the time we had available. 
    * Use the SCILAB systems at UCT.
        * While we could easily accommodation the 50 students, we would not be able to provide
          persistent access to the data. Plus, most of the radio astronomical software is primarily
          available for Linux-based installations, which would've been a problem for the Window's
          based systems in the SCILABS.
    * Use the NASSP Labs at UCT.
        * This lab comprised about 25 computers running off a single server, so we could only
          accommodate a single group at a time. We were able to install the required software and
          provide access to the data, the sheer load of having 25 students logging in at the same
          time crashed the sytem. 

Each one of these options were unfeasible, but a 4th option appeared.  Why not use the SCILAB's
and the students' own computers (or mobile devices) as _thin__clients_ for a big server? And it
turned out that I had access to a large, flexible service to spin-up transient instances of heavy
duty servers -- the African Research Cloud.

So I contacted the folks at the ARC, and we spun-up a large, single-purpose Virtual Machine, which
used the Jupyter-Hub as the primary interface. We then created accounts for each student, dumped a
copy of the data and an example notebook into each user-account's home directory, and presented the
Jupyter-Hub via an html server. Each student was able to login to the system using the web address
-- [https://arcade-jupyter-hub.uct.ac.za][arcade].

[oped]: http://www.scidev.net/sub-saharan-africa/data/opinion/big-data-opening-opportunities-africa.html
[arcade]: https://arcade-jupyter-hub.uct.ac.za
