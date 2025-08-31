---
layout: post
title:  "What is an AntennaCAT?"
summary: "A quick overview and summary of the AntennaCAT software suite that started development back in 2023, and where we see it going"
datePosted: "2025-08-02"
category: antennacat
tags: [antennacat, open_source]
---

<style>
.justified-content {
    text-align: justify;
    text-justify: inter-word;
}
</style>

<div class="justified-content">

<img src="/media/imgs/antennacat/transparent-antennaCAT-logo.png" alt="AntennaCAT logo" height="200">

<p> 
AntennaCAT started as a 2023 conference project meant to automate the CAD modeling process for several common topologies. It then quickly expanded in to a closed-loop automation system that would control EM simulation software from the outside using a custom API. From there, features including optimization and machine learning for hyper parameter tuning were added to address research needs. The AntennaCAT software has now been released open-source, free to use, and as a continuing project. This software suite was designed to lower the barrier to entry into a traditionally difficult field. And to support that, I am using these blog-style posts to explain the mechanics and inner workings of our work on this software in a less formal technical lens than my  <a href="https://scholarscompass.vcu.edu/etd/7841/">2024 dissertation</a> or the <a href="https://github.com/LC-Linkous/AntennaCalculationAutotuningTool/wiki">official AntennaCAT wiki</a>.
</p>

<p> 
The initial concept for what would be AntennaCAT started with Ansys HFSS and simulating rectangular patch antennas. Ansys HFSS is an electromagnetic (EM) simulation software used to calculate how an antenna (or radio-frequency-based technology) will operate in the real world. These simulations are based on computer assisted design (CAD) modeling where all materials in a design are mirrored digitally, even down to how individual materials respond to electrical signals (or waves). When a design is modeled as true-to-life as possible, the simulation results will be highly accurate due to the fact that it is possible to calculate an electrical (or magnetic, etc.) wave propagates in different materials, such as air.  
</p>

<p>
When an antenna design can be fully calculated, it is called an 'analytical' design. Common examples of fully analytical (or mathematically defined) designs are shown below in Fig 1. AntennaCAT includes a built-in calculator for the two designs on the left and right sizes, and the middle bowtie design is included in a replication study. All three designs have physical parameters (such as the length of their sides, or the gaps between elements) that can be calculated based on a target frequency. Simulation is typically used to check for any variations that happen between the mathematical calculations and the built design that might be caused by differences in material quality, manufacturer tolerances, or unique environmental needs. 
</p>

<figure>
<img src="/media/imgs/antenna_design/antenna_examples_simple1.png" alt="Three stylized antenna shapes with labels for variables." style="width:500px">
<figcaption>Fig.1 - Simplified antenna topologies with labels for changeable physical variables. From left to right: half-wave dipole, planar bowtie, and strip-fed rectangular patch antennas </figcaption>
</figure> 

<br>

<p>
Knowing that this relation between design, calculation, simulation, and real world results existed, we began looking at how to automate the 'tuning' process needed to bring the simulation inline with the desired design. For instance, the rectangular patch antenna equations consider the length and width of the rectangle, the depth of the substrate (the material between the ground plane and the front conductor), and the electrical properties. But while there are several common preferences for deciding the length and width of the gap (the notches on either side of the strip feed in Fig. 1), there really isn't any set equation for that feature (even including the preferences for L/4 as a starting point for the cut). Which makes simulation a highly appealing method for iterating through designs to find a candidate for a real-world experiment.
</p>

<p>
However, as the number of changeable features in the antenna design grows, so does the number of iterations that are likely needed to find a solution. Which highlights the need for automating the design process. EM simulation software suites such as Ansys often have some type of parameter sweep functionality pre-built in, but it will vary based on the software how much control a user has over the search process, stop conditions, and the data logging. AntennaCAT was created to address this gap, with the additional benefit of being able to create custom optimizers or implement those in popular literature (we created 12 base optimizers to start with). Now that AntennaCAT has been released as open-source (officially), we are working to implement some features suggested by initial student volunteer testers, and to reintegrate the hooks for other EM simulation software beyond the unit testing. Other optimizers, replication studies, and project features are also being implemented as the software develops. 
</p>

