"""Public synthetic reference demonstrator for Cortex Spatial Intelligence.

This module is independently written for public review. It is not the private
production SDK and does not reproduce proprietary implementation code.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import heapq
import json
from pathlib import Path
from typing import Any, Iterable


class ReferenceInputError(ValueError):
    """Raised when a public-demo input violates the documented contract."""


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _parse_utc(value: str) -> datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ReferenceInputError("timestamps must be UTC ISO-8601 values ending in Z")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ReferenceInputError("invalid UTC ISO-8601 timestamp") from exc
    return parsed.astimezone(timezone.utc)


@dataclass(frozen=True)
class Graph:
    nodes: dict[str, dict[str, Any]]
    adjacency: dict[str, tuple[tuple[str, float], ...]]

    @classmethod
    def from_fixture(cls, fixture: dict[str, Any]) -> "Graph":
        nodes: dict[str, dict[str, Any]] = {}
        for node in fixture.get("nodes", []):
            node_id = node.get("id")
            if not isinstance(node_id, str) or not node_id:
                raise ReferenceInputError("every node requires a non-empty id")
            if node_id in nodes:
                raise ReferenceInputError(f"duplicate node id: {node_id}")
            if node.get("traversable", True) is not True:
                continue
            nodes[node_id] = deepcopy(node)

        adjacency: dict[str, list[tuple[str, float]]] = {node_id: [] for node_id in nodes}
        for edge in fixture.get("edges", []):
            a, b, distance = edge.get("a"), edge.get("b"), edge.get("distance_m")
            if a not in nodes or b not in nodes:
                raise ReferenceInputError(f"edge references an unknown or blocked node: {a}-{b}")
            if not isinstance(distance, (int, float)) or distance <= 0:
                raise ReferenceInputError("edge distances must be positive numbers")
            adjacency[a].append((b, float(distance)))
            adjacency[b].append((a, float(distance)))

        frozen = {
            node_id: tuple(sorted(neighbors, key=lambda item: (item[0], item[1])))
            for node_id, neighbors in adjacency.items()
        }
        return cls(nodes=nodes, adjacency=frozen)

    def require_node(self, node_id: str) -> None:
        if node_id not in self.nodes:
            raise ReferenceInputError(f"unknown or non-traversable node: {node_id}")

    def shortest_path(self, start: str, end: str) -> tuple[float, list[str]]:
        self.require_node(start)
        self.require_node(end)
        queue: list[tuple[float, tuple[str, ...], str]] = [(0.0, (start,), start)]
        best: dict[str, tuple[float, tuple[str, ...]]] = {start: (0.0, (start,))}

        while queue:
            distance, path_key, node = heapq.heappop(queue)
            if best.get(node) != (distance, path_key):
                continue
            if node == end:
                return distance, list(path_key)
            for neighbor, weight in self.adjacency[node]:
                candidate = (distance + weight, path_key + (neighbor,))
                prior = best.get(neighbor)
                if prior is None or candidate < prior:
                    best[neighbor] = candidate
                    heapq.heappush(queue, (candidate[0], candidate[1], neighbor))

        raise ReferenceInputError(f"unreachable destination: {end}")


def load_fixture(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _merchandise_index(fixture: dict[str, Any]) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for item in fixture.get("merchandise", []):
        sku = item.get("sku")
        node_id = item.get("node_id")
        if not isinstance(sku, str) or not sku:
            raise ReferenceInputError("every merchandise record requires a SKU")
        if sku in index:
            raise ReferenceInputError(f"duplicate merchandise SKU: {sku}")
        index[sku] = deepcopy(item)
        index[sku]["node_id"] = node_id
    return index


def _concat_paths(paths: Iterable[list[str]]) -> list[str]:
    result: list[str] = []
    for path in paths:
        result.extend(path if not result else path[1:])
    return result


def plan_route(
    fixture: dict[str, Any],
    *,
    workflow: str,
    start_node: str,
    skus: list[str],
    end_node: str,
) -> dict[str, Any]:
    """Plan a deterministic synthetic shopper or picker route."""
    before = canonical_hash({"fixture": fixture, "skus": skus})
    if workflow not in {"shopper", "picker"}:
        raise ReferenceInputError("workflow must be shopper or picker")
    if not skus:
        raise ReferenceInputError("at least one SKU is required")

    graph = Graph.from_fixture(fixture)
    merchandise = _merchandise_index(fixture)
    graph.require_node(start_node)
    graph.require_node(end_node)

    unresolved = sorted({sku for sku in skus if sku not in merchandise})
    if unresolved:
        raise ReferenceInputError(f"unknown SKU(s): {', '.join(unresolved)}")

    remaining = [
        {"sku": sku, "node_id": merchandise[sku]["node_id"], "request_index": index}
        for index, sku in enumerate(skus)
    ]
    current = start_node
    ordered: list[dict[str, Any]] = []
    legs: list[dict[str, Any]] = []

    while remaining:
        candidates = []
        for item in remaining:
            distance, path = graph.shortest_path(current, item["node_id"])
            candidates.append((distance, item["node_id"], item["sku"], item["request_index"], path, item))
        distance, _, _, _, path, selected = min(candidates)
        ordered.append({
            "sku": selected["sku"],
            "destination_node": selected["node_id"],
            "distance_from_previous_m": distance,
        })
        legs.append({"from": current, "to": selected["node_id"], "distance_m": distance, "path": path})
        current = selected["node_id"]
        remaining.remove(selected)

    final_distance, final_path = graph.shortest_path(current, end_node)
    legs.append({"from": current, "to": end_node, "distance_m": final_distance, "path": final_path})
    result = {
        "reference_contract_version": "0.1",
        "implementation": "independent-public-reference",
        "workflow": workflow,
        "map_id": fixture.get("map_id"),
        "map_version": fixture.get("map_version"),
        "ordered_stops": ordered,
        "legs": legs,
        "full_path": _concat_paths(leg["path"] for leg in legs),
        "total_distance_m": round(sum(leg["distance_m"] for leg in legs), 6),
        "evidence": {
            "ordering_rule": "nearest reachable destination by graph distance",
            "tie_breakers": ["destination_node", "sku", "original_request_position"],
            "route_algorithm_disclosure": "standard deterministic reference search; production implementation not included",
        },
    }
    result["result_sha256"] = canonical_hash(result)
    result["input_immutability_verified"] = before == canonical_hash({"fixture": fixture, "skus": skus})
    return result


def plan_stocking(
    fixture: dict[str, Any],
    *,
    bay_node: str,
    line_items: list[dict[str, Any]],
    sequence: str = "closest-first",
    end_node: str | None = None,
) -> dict[str, Any]:
    """Plan a synthetic stocking route using graph distance from the bay."""
    before = canonical_hash({"fixture": fixture, "line_items": line_items})
    if sequence not in {"closest-first", "farthest-first"}:
        raise ReferenceInputError("sequence must be closest-first or farthest-first")
    if not line_items:
        raise ReferenceInputError("at least one stocking line is required")

    graph = Graph.from_fixture(fixture)
    merchandise = _merchandise_index(fixture)
    graph.require_node(bay_node)
    if end_node is not None:
        graph.require_node(end_node)

    normalized: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for index, item in enumerate(line_items):
        line_id = item.get("line_id", f"line-{index + 1}")
        sku = item.get("sku")
        quantity = item.get("quantity")
        if line_id in seen_ids:
            raise ReferenceInputError(f"duplicate line_id: {line_id}")
        seen_ids.add(line_id)
        if sku not in merchandise:
            raise ReferenceInputError(f"unknown SKU: {sku}")
        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
            raise ReferenceInputError(f"quantity for {line_id} must be a positive integer")
        destination = merchandise[sku]["node_id"]
        distance, path = graph.shortest_path(bay_node, destination)
        normalized.append({
            "line_id": line_id,
            "sku": sku,
            "quantity": quantity,
            "destination_node": destination,
            "distance_from_bay_m": distance,
            "bay_path": path,
            "request_index": index,
        })

    if sequence == "closest-first":
        normalized.sort(key=lambda item: (item["distance_from_bay_m"], item["destination_node"], item["sku"], item["request_index"]))
    else:
        normalized.sort(key=lambda item: (-item["distance_from_bay_m"], item["destination_node"], item["sku"], item["request_index"]))

    grouped: list[dict[str, Any]] = []
    for item in normalized:
        if grouped and grouped[-1]["destination_node"] == item["destination_node"]:
            grouped[-1]["lines"].append({key: item[key] for key in ("line_id", "sku", "quantity")})
        else:
            grouped.append({
                "destination_node": item["destination_node"],
                "distance_from_bay_m": item["distance_from_bay_m"],
                "lines": [{key: item[key] for key in ("line_id", "sku", "quantity")}],
            })

    current = bay_node
    legs: list[dict[str, Any]] = []
    for stop in grouped:
        distance, path = graph.shortest_path(current, stop["destination_node"])
        legs.append({"from": current, "to": stop["destination_node"], "distance_m": distance, "path": path})
        current = stop["destination_node"]
    if end_node is not None:
        distance, path = graph.shortest_path(current, end_node)
        legs.append({"from": current, "to": end_node, "distance_m": distance, "path": path})

    result = {
        "reference_contract_version": "0.1",
        "implementation": "independent-public-reference",
        "workflow": "stocker",
        "map_id": fixture.get("map_id"),
        "map_version": fixture.get("map_version"),
        "bay_node": bay_node,
        "sequence": sequence,
        "ordered_stops": grouped,
        "legs": legs,
        "full_path": _concat_paths(leg["path"] for leg in legs),
        "total_distance_m": round(sum(leg["distance_m"] for leg in legs), 6),
        "evidence": {
            "ranking_distance": "shortest traversable graph distance from bay",
            "tie_breakers": ["destination_node", "sku", "original_request_position"],
            "post_ranking_behavior": "fixed order reconstructed; no silent re-optimization",
        },
    }
    result["result_sha256"] = canonical_hash(result)
    result["input_immutability_verified"] = before == canonical_hash({"fixture": fixture, "line_items": line_items})
    return result


def evaluate_promotions(
    fixture: dict[str, Any],
    *,
    evaluation_timestamp: str,
    location_id: str,
    current_node: str,
    route_corridor: list[str],
    campaigns: list[dict[str, Any]],
    promotions_enabled: bool = True,
) -> dict[str, Any]:
    """Evaluate synthetic campaign eligibility without accepting or returning a route plan."""
    before = canonical_hash({"fixture": fixture, "route_corridor": route_corridor, "campaigns": campaigns})
    now = _parse_utc(evaluation_timestamp)
    graph = Graph.from_fixture(fixture)
    merchandise = _merchandise_index(fixture)
    graph.require_node(current_node)
    for node in route_corridor:
        graph.require_node(node)

    eligible: list[dict[str, Any]] = []
    suppressed: list[dict[str, Any]] = []
    for raw in campaigns:
        campaign = deepcopy(raw)
        campaign_id = str(campaign.get("campaign_id", ""))
        reason: str | None = None
        if not promotions_enabled:
            reason = "promotions-disabled"
        elif campaign.get("approval_state") != "approved":
            reason = "not-approved"
        elif campaign.get("lifecycle_state") != "active":
            reason = "not-active"
        elif location_id not in campaign.get("location_scope", []):
            reason = "location-out-of-scope"
        elif campaign.get("sku") not in merchandise:
            reason = "missing-authoritative-merchandise"
        else:
            start = _parse_utc(campaign.get("campaign_start", ""))
            end = _parse_utc(campaign.get("campaign_expiration", ""))
            if not start <= now < end:
                reason = "outside-effective-period"
            else:
                destination = merchandise[campaign["sku"]]["node_id"]
                if campaign.get("destination_node") != destination:
                    reason = "destination-mismatch"
                elif destination not in route_corridor:
                    reason = "outside-route-corridor"
                elif campaign.get("source") == "sponsored-placement" and not campaign.get("disclosure", {}).get("sponsored", False):
                    reason = "missing-sponsorship-disclosure"
                else:
                    distance, _ = graph.shortest_path(current_node, destination)
                    threshold = campaign.get("proximity_threshold_m", 15)
                    if not isinstance(threshold, (int, float)) or threshold <= 0 or threshold > 100:
                        reason = "invalid-proximity-threshold"
                    elif distance > threshold:
                        reason = "outside-proximity-boundary"
                    else:
                        eligible.append({
                            "campaign_id": campaign_id,
                            "source": campaign.get("source"),
                            "sku": campaign.get("sku"),
                            "destination_node": destination,
                            "proximity_m": distance,
                            "placement_tier": int(campaign.get("placement_tier", 0)),
                            "remaining_validity_seconds": int((end - now).total_seconds()),
                            "disclosure": deepcopy(campaign.get("disclosure")),
                            "decision": "eligible",
                        })
        if reason is not None:
            suppressed.append({"campaign_id": campaign_id, "decision": "suppressed", "reason": reason})

    source_order = {"weekly-sale": 0, "sponsored-placement": 1}
    eligible.sort(key=lambda item: (
        item["proximity_m"],
        -item["placement_tier"],
        source_order.get(item["source"], 99),
        -item["remaining_validity_seconds"],
        item["campaign_id"],
    ))
    result = {
        "reference_contract_version": "0.1",
        "implementation": "independent-public-reference",
        "evaluation_timestamp": evaluation_timestamp,
        "eligible_promotions": eligible,
        "suppressed_promotions": sorted(suppressed, key=lambda item: item["campaign_id"]),
        "route_protection": {
            "route_plan_accepted": False,
            "replacement_route_returned": False,
            "explicit_route_request_required_after_add": True,
        },
        "ranking": ["proximity", "placement-tier", "source-policy", "remaining-validity", "campaign-id"],
    }
    result["result_sha256"] = canonical_hash(result)
    result["input_immutability_verified"] = before == canonical_hash({"fixture": fixture, "route_corridor": route_corridor, "campaigns": campaigns})
    return result

