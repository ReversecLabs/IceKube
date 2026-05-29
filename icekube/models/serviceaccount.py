from __future__ import annotations

from functools import cached_property
from typing import Any, Dict, List, Optional, cast

from icekube.models.base import RELATIONSHIP, Resource
from icekube.models.secret import Secret
from icekube.relationships import Relationship
from pydantic import computed_field


class ServiceAccount(Resource):
    supported_api_groups: List[str] = [""]

    @computed_field  # type: ignore
    @cached_property
    def secrets(self) -> List[Secret]:
        secrets = []
        raw_secrets = self.data.get("secrets") or []

        for secret in raw_secrets:
            secrets.append(
                Secret(name=secret.get("name", ""), namespace=self.namespace),
            )

        return secrets

    @computed_field  # type: ignore
    @cached_property
    def cloud_identity(self) -> Optional[str]:
        keys = ["eks.amazonaws.com/role-arn", "azure.workload.identity/client-id"]

        for key in keys:
            if key in self.annotations:
                return cast(str, self.annotations[key])

        return None

    @property
    def db_labels(self) -> Dict[str, Any]:
        return {
            **super().db_labels,
            "cloud_identity": self.cloud_identity,
        }

    def relationships(
        self,
        initial: bool = True,
    ) -> List[RELATIONSHIP]:
        relationships = super().relationships()

        # This is to account for secrets that we have not got the metadata for
        # If we have the metadata, the relevant relationship will be generated from that
        # resource
        QUERY = "MATCH ({prefix}:Secret {{ namespace: ${prefix}_namespace, name: ${prefix}_name }})"
        QUERY += " WHERE {prefix}.raw IS NULL "

        if initial:
            relationships += [(self, Relationship.REFERENCES, x) for x in self.secrets]
        else:
            relationships += [
                (
                    (
                        QUERY,
                        {"namespace": cast(str, x.namespace), "name": x.name},
                    ),
                    Relationship.AUTHENTICATION_TOKEN_FOR,
                    self,
                )
                for x in self.secrets
            ]
        return relationships
