---
layout: post
title:  "Introducing AntennaCAT"
summary: "AntennaCAT is now live! The 2025 release is the official full release of the AntennaCAT software suite."
datePosted: "2025-08-01"
category: antennacat
tags: [antennacat, open_source, research, software]
---

<style>
.justified-content {
    text-align: justify;
    text-justify: inter-word;
}
</style>

<div class="justified-content">

<p>
AntennaCAT is now live!
</p>
<p>
After several conference publications and (finally!!) a completed dissertation, the open-source AntennaCAT software is now live and free to use on GitHub at <a href="https://github.com/LC-Linkous/AntennaCalculationAutotuningTool">https://github.com/LC-Linkous/AntennaCalculationAutotuningTool</a>. 
</p>

<p> 
The Antenna Calculation and Autotuning Tool (AntennaCAT) software suite is a comprehensive implementation of machine learning to automate, evaluate, and optimize the antenna design process using EM simulation software. It utilizes a combined antenna designer pre-loaded with replication studies and internal calculator to accelerate the CAD construction and EM simulation of several common topologies, while eliminating model disparity for automated data collection. In particular, this work includes the capability to create and export structured datasets from the aforementioned EM software for iterative improvement and includes an expandable selection of optimizers. AntennaCAT is designed with three things in mind: accessibility, adaptability, and experimentation. 
</p>
<p>
The AntennaCAT software suite and related examples have appeared in the following publications:
    <ol>
    <li>L. Linkous, E. Karincic, J. Lundquist and E. Topsakal, "Automated Antenna Calculation, Design and Tuning Tool for HFSS," _2023 United States National Committee of URSI National Radio Science Meeting (USNC-URSI NRSM)_, Boulder, CO, USA, 2023, pp. 229-230, doi: 10.23919/USNC-URSINRSM57470.2023.10043119. </li>
    <li>E. Karincic, L. Linkous, and E. Topsakal , "Generalized Machine-Learning Particle Swarm Optimization Antennas for CBRS," 2023 United States National Committee of URSI National Radio Science Meeting (USNC-URSI NRSM), Boulder, CO, USA, 2023 https://www.usnc-ursi-archive.org/nrsm/2023/papers/1065.pdf (supporting material demonstrating the early genetic algorithm) </li>
    <li>L. Linkous, J. Lundquist and E. Topsakal, "AntennaCAT: Automated Antenna Design and Tuning Tool," _2023 IEEE USNC-URSI Radio Science Meeting (Joint with AP-S Symposium)_, Portland, OR, USA, 2023, pp. 89-90, doi: 10.23919/USNC-URSI54200.2023.10289238. </li>
    <li>L. Linkous, J. Lundquist, M. Suche, and E. Topsakal, "Machine Learning Assisted Hyperparameter Tuning for Optimization," _2024 IEEE International Symposium on Antennas and Propagation and ITNC-USNC-URSI Radio Science Meeting_, Florence, Italy, 2024 </li>
    <li>L. Linkous and E. Topsakal, "Machine Learning Assisted Optimization Methods for Automated Antenna Design," _2024 United States National Committee of URSI National Radio Science Meeting (USNC-URSI NRSM)_, Boulder, CO, USA, 2024, pp. 377-378, doi: 10.23919/USNC-URSINRSM60317.2024.10464597. </li>
    <li>L. Linkous, “Machine Learning Assisted Optimization for Calculation and Automated Tuning of Antennas,” VCU Scholars Compass, 2024. https://scholarscompass.vcu.edu/etd/7841/</li>
    <li>L. Linkous, J. Lundquist, M. J. Suche and E. Topsakal, "AntennaCAT: Automated antenna design with machine learning-assisted optimization [Open Source]," in _IEEE Antennas and Propagation Magazine_, vol. 67, no. 3, pp. 87-96, June 2025, doi: 10.1109/MAP.2025.3560851 </li>
    </ol>

</p>

<p> 
In addition to the main repository, a <a href="https://github.com/LC-Linkous/AntennaCalculationAutotuningTool/wiki">AntennaCAT wiki on GitHub</a> has been created with full documentation of all steps from how to access and download the AntennaCAT code, to how to run it, to how to customize designs. These wiki pages include a mix of overview and tutorials to cover the range of features. As this is a dynamic and developing project (as is most early open-source projects), the wiki will have the most up to date descriptions of AntennaCAT and it's features. 
</p> 
<p> 
Posts, such as this one, will go into detail of specific, core AntennaCAT features and the reasoning behind some of the design choices. The posts are much less formal than the released publications, less technically detailed than many of the wiki articles, and are meant to offer insight into how the logic of the software and integration works. Posts and tutorials related to AntennaCAT will typically be published with the <a href=" https://lc-linkous.github.io/tags/antennacat/">antennacat tag</a>.

</p> 

<p>
Note: This post was private until magazine publication (July 2025), and then released publicly Aug. 2025
</p>
