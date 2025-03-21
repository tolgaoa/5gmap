# MobiCom 2025 - Artifact Submission - 5G-MAP: Demystifying the Performance Implications of Cloud-Based 5G Core Deployments

This repository contains the instructions for:
- deployment of the 5G-MAP integrated OpenAirInterface 5G Core
- the source code of the 5G-MAP Side Car Proxy

**Note**
- See Appendix D for details on the user traffic patterns

- All the Docker image names have been anonymized and will NOT work.


------------------------------------------------------------------------------
## Infrastructure Setup

The AWS infrastructure used is depicted below.

![Alt text](figures/githubdesc.png?raw=true)

In any given AZ, we start by creating a Bastion node that serves as the workstation to create and operate over the Kubernetes cluster. The remaining VMs are distributed into AZs and edge zones depending on user requirements. The Bastion node is the sole operation center and contains the cluster.yml file which is used to create the Kubernetes cluster. 

------------------------------------------------------------------------------
## Feature Set

To emulate 5G network slices we utilize the OAI 5G core and the gNBSIM entity to create end-to-end packet data unit (PDU) sessions with multiple users. The deployment scheme is given below.

![Alt text](figures/oaiflow2.png?raw=true)

To be able to accurately reflect the load on the user plane of the 5GC, real traffic patterns are used from actual use cases. To capture the traffic patterns pertaining to each use case, we use an OpenWRT router and filter out the downlink and uplink packets related to the desired connection. The utilized patterns are given below.

![Alt text](figures/traffictypes.png?raw=true)



