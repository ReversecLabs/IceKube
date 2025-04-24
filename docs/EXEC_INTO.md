# EXEC_INTO

### Overview

This attack path aims to locate subjects which can execute into pods. An attacker could use this to gain a foothold in a running pod.

### Description

An attacker with the ability to execute commands within a pod could gain access to the data within. This would include access to its processes, filesystem, network position, etc. This could be used as a foothold for further attacks within the cluster.

Executing commands in a pod requires two permissions. The first is `create` or `get` on `pods/exec` and the second is `get` on `pods`. Both of those permissions should affect the target pod.

The fact that read-only permissions can be used to exec into a pod is a side-effect of how websockets work, this is further discussed by [Rory McCune](https://raesene.github.io/blog/2024/11/11/When-Is-Read-Only-Not-Read-Only/).

### Defense

RBAC permissions regarding the outlined permissions should be reviewed. Access should be restricted to required entities.

### Cypher Deep-Dive

```cypher
MATCH (src)-[:GRANTS_EXEC_CREATE|GRANTS_EXEC_GET]->(dest:Pod)<-[:GRANTS_GET]-(src)
```

The above query finds all resources (`src`) that have `GRANTS_EXEC_CREATE` or `GRANTS_EXEC_GET` and `GRANTS_GET` on a Pod (`dest`). The two relationships map to the two required permissions for executing commands within a pod.
