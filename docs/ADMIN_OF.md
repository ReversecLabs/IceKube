# ADMIN_OF

### Overview

This rule establishes an attack path relationship between a cluster role binding and the cluster, if the cluster role binding is associated with a cluster role that grants all permissions. This allows for easy identification of sensitive cluster role bindings.

### Description

Cluster role bindings that allocate all permissions through their cluster role are highly sensitive, as an attacker that has gained access to a subject of this binding would be able to perform any action within the cluster.

### Defense

Follow the principle of least privilege when assigning permissions to subjects.

### Cypher Deep-Dive

```cypher
MATCH (src:ClusterRoleBinding {{gives_cluster_admin: true}})-[:WITHIN_CLUSTER]-(dest:Cluster)
```

Finds all ClusterRoleBinding (`src`) that have the property `gives_cluster_admin` set to true, indicating that they are associated with a ClusterRole that grants all permissions. The `WITHIN_CLUSTER` relationship connects the ClusterRoleBinding to the Cluster (`dest`) it belongs to.

The property is set by IceKube if the ClusterRole associated with it has a rule with the following:

```yaml
- apiGroups:
  - "*"
  resources:
  - "*"
  verbs:
  - "*"
```
