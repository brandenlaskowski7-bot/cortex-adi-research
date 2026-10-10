# Cortex Spatial Intelligence: A Governed Public Reference for Deterministic Indoor Workflows

**Author:** Branden Laskowski  
**Affiliation:** Cortex Agentics Global Inc.  
**Release:** Public peer-review candidate v0.1  
**Date:** 2026-10-10

## Abstract

Indoor navigation products often combine map truth, changing merchandise locations, workflow policy, positioning observations, and commercial messaging in ways that are difficult to audit. Cortex Spatial Intelligence proposes a separation-of-authority model in which an immutable, versioned traversable graph is distinct from dynamic merchandise data, workflow rules, positioning inputs, and an optional promotion policy. This release provides an independently written public reference implementation over a wholly synthetic store. It demonstrates deterministic shopper and picker routing, graph-distance-based stocking sequences, and route-protected promotion decisions. It does not disclose or reproduce the private production implementation. The package supplies explicit inputs, canonical output hashes, 22 deterministic tests, limitations, and a claims ledger so reviewers can distinguish public evidence from private production evidence and proposed commercial outcomes.

## 1. Review question

Can several indoor workflows share governed spatial inputs while keeping routing deterministic, promotion logic unable to control a route, and proprietary production internals undisclosed?

The public package addresses that narrow question. It does not claim production readiness, real-world performance, sales lift, labor savings, or independent validation.

## 2. Boundary model

The architecture separates:

1. authoritative spatial truth: versioned traversable nodes and weighted edges;
2. dynamic merchandise truth: SKU-to-destination records kept outside the floor map;
3. workflow policy: shopper, fulfillment-picker, and stocker behaviors;
4. positioning observations: current location supplied as an input; and
5. promotion policy: an optional evaluator that may inspect route context but may not mutate or replace a route.

The reference implementation consumes a synthetic fixture. It contains no real retailer map, customer record, movement history, operational feed, or production integration.

## 3. Deterministic methods

### 3.1 Traversable graph distance

All path lengths are calculated from positive edge weights in the traversable graph. The public reference uses a standard shortest-path search with a lexicographic path key as a stable tie-break. Straight-line coordinate distance is not used to order stocking destinations.

### 3.2 Shopper and picker ordering

From the current node, the reference selects the reachable requested destination with the smallest graph distance. Equal candidates are resolved by destination node, SKU, and original request position. It repeats until every requested destination is visited, then appends the path to the selected end node.

This is a reviewable reference rule, not a disclosure of the private production optimizer.

### 3.3 Stocking and replenishment

Each inventory line is resolved to a merchandise destination. Its distance is measured from the selected receiving or staging bay using the graph. `closest-first` sorts ascending; `farthest-first` sorts descending. Equal distances use destination node, SKU, and original request position. Lines sharing a destination are grouped without losing line identity or quantity. Once ordered, executable graph paths are reconstructed through the stops without silently optimizing them into a new order.

### 3.4 Governed promotions

Campaign evaluation requires an explicit UTC timestamp and checks lifecycle, approval, location scope, authoritative SKU destination, proximity, route-corridor relevance, sponsorship disclosure, and the global enable switch. Eligible campaigns are ranked by proximity, placement tier, source policy, remaining validity, and campaign ID.

Paid tier cannot bypass eligibility. The evaluator accepts a route corridor but not a `RoutePlan`; its response contains decisions and evidence but no replacement route. A promoted product can enter routing only through a later, explicit route request outside the evaluator.

## 4. Evidence and reproducibility

The public suite contains 22 tests covering repeatability, input rejection, graph-distance stocking order, grouping, fixed-order path reconstruction, lifecycle suppression, sponsorship disclosure, campaign tie-breaking, input immutability, and promotion route protection. The release evidence records the commands, environment, results, and SHA-256 hashes of allowlisted files.

The private production repository has separately reported 67 unit tests and 3 component tests passing at commit `2488754d3fd8e5741616309b3efd03ebe8b084c8`. That statement is classified as private production evidence: the underlying source is not included and the result cannot be independently reproduced from this package.

## 5. Results

For the release candidate:

- all 22 public reference tests pass;
- repeated identical requests produce equivalent structured results and hashes;
- stocking order follows graph distance from the bay in both supported directions;
- shared destinations preserve each line and quantity;
- sponsored campaigns without affirmative disclosure are suppressed; and
- promotion evaluation neither accepts nor returns a route plan.

These results apply only to the included synthetic fixture and public reference implementation.

## 6. Privacy, safety, and commercial governance

The reference uses no personal data. Production designs should minimize promotion evidence, prefer session-scoped or pseudonymous identifiers, avoid retaining precise movement histories unless separately authorized, and give customer preference, accessibility, safety, and frequency controls priority over commercial placement.

Purchased promotional space is governed inventory, not ownership of navigation. A payment may affect ranking only after every noncommercial eligibility requirement has passed.

## 7. Limitations and falsifiability

The public graph is small, synthetic, and single-floor. It has no live positioning, accessibility overlay, congestion, hazards, multi-floor transitions, retailer feed, mobile client, or production load. The reference promotion implementation does not reproduce a complete production frequency or preference system. Reviewers should treat any operational or financial outcome as unproven until measured in an authorized pilot with a declared protocol.

A reviewer can falsify the bounded deterministic claims by supplying a documented input for which identical evaluations differ, a stocking destination is ranked by geometry rather than graph distance, a fixed stocking order is changed during path reconstruction, an ineligible paid campaign is displayed, or a promotion evaluation returns or mutates a route.

## 8. Conclusion

The release demonstrates a public, executable contract for governed indoor spatial workflows without exposing the private engine. Its contribution is the observable separation between spatial truth, merchandise truth, workflow policy, positioning context, and optional commercial policy, together with deterministic evidence that reviewers can inspect and challenge.

