---
author: Charles Chang
title: 'Registering Initiators and "Host Access" Configuration on EMC Unisphere with UCS Compute Node'
tags: ucs, emc, servers, storage
gh_issue_number: 1460
---

### Registering UCS Compute Initiators and Configuring Host Access within EMC Unisphere GUI ###

#### Prerequisites ####

This blog assumes the UCS environment is setup and ready for Boot from SAN. UCS compute node are ready for ESXi installation. UCS service profile are assigned to each compute node with the proper BIOS configuration for vSphere installation.

#### Introduction ####
The goal of this blog is to build a new UCS environment with 2 chassis and 4 compute node in each chassis, and connect the initiators for each compute node. If zoning is done correctly on the fiber switch, then the intitators should register automatically within the EMC Unisphere GUI. The main issue associated with boot from SAN setup using EMC storage is the "Host Access" setup for each ESXi. Unfortunately, the "Host Access" configuration does not register automatically. Initially, the ESXi with manually created "Host Access" will work initially, but the next time you boot from SAN, it will display the dreaded error "boot device cannot be found". To avoid this, you would have to get the "Host Access" to register on EMC Unisphere GUI as "Auto".

##### On EMC Unisphere GUI #####

1\. First step is to manually create an access for each esxi host on EMC Unisphere GUI. On the screenshot, the "Host Access" will register as manual.

<img src="/blog/2018/10/10/EMC-Unity-Storage-Register-Initiator/image1.png" alt="Create Access for each host" />

2\. Next step is to carve out storage for each compute node which the ESXi will install onto. For the test I created a 10GB volume for each ESXi Host on EMC Unisphere GUI.

3\. The next step is to manually add the initiators to each host created. The screenshot below will display the initiators registering from each UCS compute node to EMC storage. This is a automated process as long as the Initiators are setup properly within the UCS manager.

<img src="/blog/2018/10/10/EMC-Unity-Storage-Register-Initiator/image2.png" alt="Initiator registering automatically to EMC Unisphere GUI" />

4\. Next step is to open the "Host Access" configuration for each host. Confirm if the correct initiators are attached to each host. Once you assign the correct initiators for each "Host Access", continue on to next step.

##### On UCS Manager #####

1\. The next step is to run the ESXi ISO using the virtual console within the UCS Manager on the compute node that need ESXi installed.

2\. Once the ESXi ISO installation begins, the usual questions are asked, like root password, host name, network information, etc. 

3\. The step we would need to address is the location of the ESXi installation.

4\. Once you reach this section, the compute node should automatically pick up the LUNs you created within the EMC Unisphere GUI.

<img src="/blog/2018/10/10/EMC-Unity-Storage-Register-Initiator/image3.png" alt="Select Storage to install ESXi" />

5\. Go ahead and select the LUN associated with the compute node. Should be able to locate the correct NAA from within the EMC Unisphere GUI and compare to what is displayed on the ESXi install to make sure you have the correct volume. 

6\. Once you complete the selection of the disk, this should take you to the end of the ESXi installation which would ask you to disconnect the CDROM/ISO and reboot the host.

7\. Go ahead and reboot the ESXI host.

8\. Before adding the new ESXi to vSphere, go ahead and console access into the ESXi host and make sure the ESXi network and host name is setup correctly.

##### On vSphere #####

1\. Next step is to head over to vSphere and add the new ESXi host to vSphere.

2\. Go ahead and do the usual configuration within vSphere like creating the datacenter, cluster, network in case, etc. if this is a new vSphere build out. If not, then go to the next step.

3\. Once you add the new ESXi host, and the new host is pingable, go ahead and put the new ESXi host into maintenance mode.

##### Back to EMC Unisphere GUI #####

1\. Next step is to head back to the EMC Unisphere GUI where you created the "Host Access" for this new ESXi host.

2\. Once you are back to the "Host Access" section on Unisphere, go ahead and delete the manually create "Host Access" we created in step 1. As you could see below "Host Access" Type is "Manual" which needs to be set to "Auto".

<img src="/blog/2018/10/10/EMC-Unity-Storage-Register-Initiator/image4.png" alt="Delete Host Access on EMC" />

3\. Probably would need remove the LUNs and Initiators from the "Host Access" before deleting the "Host Access" entry. 

##### Back to vSphere #####

1\. Once the Manually created "Host Access" is deleted, while the ESXi host still in maintenance mode, go ahead and rescan the datastore and storage within the vSphere client or web GUI. 

##### Back to EMC Unisphere GUI #####

1\. Once you rescan the storage within vSphere, head back to the EMC Unisphere GUI and check if the host automatically register back to the "Host Access" section on EMC Unisphere GUI. The screenshot below will depict some host under "Access" on EMC Unisphere GUI setup as "Auto".

<img src="/blog/2018/10/10/EMC-Unity-Storage-Register-Initiator/image5.png" alt="Properly Registered Host" />

2\. Also confirm under Access on EMC Unisphere GUI, if the correct initiators are attached and also LUN ID is set to 0 for boot to san. If all goes well, then the ESXi host should be able to boot from SAN.

3\. Repeat these steps if adding additional host. 

#### Summary ####

Initially the expectation is that the initiator would connect automatically without intervention but some technology need a workaround to get it to work properly. The above example was based on real life experience working with Boot to SAN using EMC Unity storage along with Cisco UCS compute hardware. The beauty of the UCS environment along with shared storage adds up to superior hyper-converged environment with full redundancy and the ability to grow vertically as to horizontally which in terms save quite a bit of money. The hyper-converged encourage growth while minimizing spending on adding additional storage unit or expanding the network environment. Thus the cost of building a UCS environment with the ability to vertically grow and provide flexibility to easily manage a hyper-converged environment without causing outages during maintenance or common task during business hours is a luxury for all companies to have. 
<br>





