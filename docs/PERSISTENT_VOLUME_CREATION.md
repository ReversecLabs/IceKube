# PERSISTENT_VOLUME_CREATION

### Overview

This attack path aims to locate subjects which can create persistent volumes and can create pods in a namespace. Upon successful exploitation, an attacker would gain privileged access to nodes within the cluster.

### Description

An attacker with the ability to create persistent volumes (PV) could create one backed by paths on the underlying host, for example `/`. A claim from this PV could then be mounted into a pod as a volume. As this is a persistent volume claim (PVC), it is common for this to be permitted as part of pod security controls. It is a permitted volume type in the restricted pod security standard.

Once an attacker has deployed a pod with the PVC, they would have privileged write access to the underlying node from which there are a multitude of ways to gain full access to the host. 

### Defense

RBAC permissions to create persistent volumes. Access should be restricted to required entities. 

### Cyper Deep-Dive

```cypher
MATCH (src)-[:BOUND_TO]->(:ClusterRoleBinding)-[:GRANTS_PERSISTENTVOLUMES_CREATE]->(), (dest:Node)
WHERE (src)-[:BOUND_TO]->(:RoleBinding|ClusterRoleBinding)-[:GRANTS_PODS_CREATE|GRANTS_REPLICATIONCONTROLLERS_CREATE|GRANTS_DAEMONSETS_CREATE|GRANTS_DEPLOYMENTS_CREATE|GRANTS_REPLICASETS_CREATE|GRANTS_STATEFULSETS_CREATE|GRANTS_CRONJOBS_CREATE|GRANTS_JOBS_CREATE]->()
```

The above query finds all entities (`src`) which both have the permission to create persistent volumes and can create workloads within the cluster. The target node (`dest`) is a node within the cluster.

Workload creation is used as opposed to solely pods because various Kubernetes controllers create pods automatically from more abstract workload resources. Configuration of the workload resource also configures the created pod, thus it would allow an attacker to create the desired pod.

Workload creation includes the following:
- `pods`
- `replicationcontrollers`
- `daemonsets`
- `deployments`
- `replicasets`
- `statefulsets`
- `cornjobs`
- `jobs`
