# Public observable contract v0.1

This document describes reviewable input and output shapes. It is not a production SDK release or a compatibility promise.

## Route request

```json
{
  "workflow": "shopper",
  "start_node": "ENT",
  "skus": ["SYN-MILK", "SYN-APPLE"],
  "end_node": "CHK"
}
```

## Route result

```json
{
  "reference_contract_version": "0.1",
  "implementation": "independent-public-reference",
  "workflow": "shopper",
  "map_id": "synthetic-review-store",
  "map_version": "0.1",
  "ordered_stops": [],
  "legs": [],
  "full_path": [],
  "total_distance_m": 0,
  "evidence": {},
  "result_sha256": "...",
  "input_immutability_verified": true
}
```

## Stocking request

```json
{
  "bay_node": "BAY",
  "sequence": "closest-first",
  "line_items": [
    {"line_id": "L1", "sku": "SYN-MILK", "quantity": 4},
    {"line_id": "L2", "sku": "SYN-APPLE", "quantity": 2}
  ],
  "end_node": null
}
```

The result adds the selected sequence, ordered grouped stops, graph distance from the bay, full executable legs, total distance, and ordering evidence.

## Promotion evaluation request

```json
{
  "evaluation_timestamp": "2026-10-10T16:00:00Z",
  "location_id": "SYNTHETIC-001",
  "current_node": "B1",
  "route_corridor": ["ENT", "A1", "B1", "B2", "C1", "C2", "CHK"],
  "campaigns": [],
  "promotions_enabled": true
}
```

## Promotion evaluation result

```json
{
  "eligible_promotions": [],
  "suppressed_promotions": [],
  "route_protection": {
    "route_plan_accepted": false,
    "replacement_route_returned": false,
    "explicit_route_request_required_after_add": true
  },
  "ranking": [
    "proximity",
    "placement-tier",
    "source-policy",
    "remaining-validity",
    "campaign-id"
  ]
}
```

## Error behavior

The reference demonstrator rejects unknown nodes, unknown SKUs, invalid quantities, invalid sequence values, unreachable destinations, malformed timestamps, invalid proximity thresholds, and malformed campaign JSON. It does not partially plan a request after a fatal input error.

## Non-contractual fields

Names, exact field organization, error codes, data types, and versioning shown here may change before any commercial SDK release. Commercial compatibility is governed only by an executed license and its published SDK contract.

