from copy import deepcopy
import unittest

from reference_engine import (
    ReferenceInputError,
    canonical_hash,
    evaluate_promotions,
    load_fixture,
    plan_route,
    plan_stocking,
)


FIXTURE = load_fixture("fixtures/synthetic_store.json")
NOW = "2026-10-10T16:00:00Z"


def campaign(**changes):
    value = {
        "campaign_id": "CAMPAIGN-001",
        "source": "weekly-sale",
        "approval_state": "approved",
        "lifecycle_state": "active",
        "location_scope": ["SYNTHETIC-001"],
        "sku": "SYN-CEREAL",
        "destination_node": "B2",
        "campaign_start": "2026-10-01T00:00:00Z",
        "campaign_expiration": "2026-11-01T00:00:00Z",
        "placement_tier": 0,
        "proximity_threshold_m": 15,
        "disclosure": {"sponsored": False, "text": "Weekly sale"},
    }
    value.update(changes)
    return value


class RouteTests(unittest.TestCase):
    def test_shop_route_is_deterministic(self):
        request = dict(workflow="shopper", start_node="ENT", skus=["SYN-MILK", "SYN-APPLE"], end_node="CHK")
        first = plan_route(FIXTURE, **request)
        second = plan_route(FIXTURE, **request)
        self.assertEqual(first, second)
        self.assertEqual(first["result_sha256"], second["result_sha256"])

    def test_picker_uses_same_public_contract_shape(self):
        result = plan_route(FIXTURE, workflow="picker", start_node="ENT", skus=["SYN-BREAD"], end_node="CHK")
        self.assertEqual(result["workflow"], "picker")
        self.assertTrue(result["full_path"])

    def test_unknown_sku_is_rejected(self):
        with self.assertRaises(ReferenceInputError):
            plan_route(FIXTURE, workflow="shopper", start_node="ENT", skus=["UNKNOWN"], end_node="CHK")

    def test_unknown_node_is_rejected(self):
        with self.assertRaises(ReferenceInputError):
            plan_route(FIXTURE, workflow="shopper", start_node="MISSING", skus=["SYN-BREAD"], end_node="CHK")

    def test_inputs_are_not_mutated(self):
        fixture = deepcopy(FIXTURE)
        skus = ["SYN-MILK", "SYN-APPLE"]
        before = canonical_hash({"fixture": fixture, "skus": skus})
        plan_route(fixture, workflow="shopper", start_node="ENT", skus=skus, end_node="CHK")
        self.assertEqual(before, canonical_hash({"fixture": fixture, "skus": skus}))


class StockingTests(unittest.TestCase):
    def lines(self):
        return [
            {"line_id": "L1", "sku": "SYN-APPLE", "quantity": 2},
            {"line_id": "L2", "sku": "SYN-MILK", "quantity": 4},
            {"line_id": "L3", "sku": "SYN-BULK", "quantity": 3},
        ]

    def test_closest_first_is_default(self):
        result = plan_stocking(FIXTURE, bay_node="BAY", line_items=self.lines())
        self.assertEqual(result["sequence"], "closest-first")
        distances = [stop["distance_from_bay_m"] for stop in result["ordered_stops"]]
        self.assertEqual(distances, sorted(distances))

    def test_farthest_first(self):
        result = plan_stocking(FIXTURE, bay_node="BAY", line_items=self.lines(), sequence="farthest-first")
        distances = [stop["distance_from_bay_m"] for stop in result["ordered_stops"]]
        self.assertEqual(distances, sorted(distances, reverse=True))

    def test_graph_distance_not_euclidean_distance(self):
        result = plan_stocking(
            FIXTURE,
            bay_node="BAY",
            line_items=[
                {"line_id": "L1", "sku": "SYN-MILK", "quantity": 1},
                {"line_id": "L2", "sku": "SYN-CEREAL", "quantity": 1},
            ],
        )
        distances = {stop["destination_node"]: stop["distance_from_bay_m"] for stop in result["ordered_stops"]}
        self.assertEqual(distances["C2"], 4.0)
        self.assertEqual(distances["B2"], 7.0)

    def test_shared_destination_is_grouped(self):
        result = plan_stocking(FIXTURE, bay_node="BAY", line_items=self.lines())
        a2 = next(stop for stop in result["ordered_stops"] if stop["destination_node"] == "A2")
        self.assertEqual([line["sku"] for line in a2["lines"]], ["SYN-APPLE", "SYN-BULK"])

    def test_fixed_order_paths_are_reconstructed(self):
        result = plan_stocking(FIXTURE, bay_node="BAY", line_items=self.lines(), sequence="farthest-first")
        self.assertEqual([leg["to"] for leg in result["legs"]], [stop["destination_node"] for stop in result["ordered_stops"]])

    def test_invalid_quantity_is_rejected(self):
        with self.assertRaises(ReferenceInputError):
            plan_stocking(FIXTURE, bay_node="BAY", line_items=[{"line_id": "L1", "sku": "SYN-MILK", "quantity": 0}])

    def test_duplicate_line_id_is_rejected(self):
        with self.assertRaises(ReferenceInputError):
            plan_stocking(FIXTURE, bay_node="BAY", line_items=[
                {"line_id": "L1", "sku": "SYN-MILK", "quantity": 1},
                {"line_id": "L1", "sku": "SYN-APPLE", "quantity": 1},
            ])


class PromotionTests(unittest.TestCase):
    def evaluate(self, campaigns, **changes):
        params = dict(
            fixture=FIXTURE,
            evaluation_timestamp=NOW,
            location_id="SYNTHETIC-001",
            current_node="B1",
            route_corridor=["ENT", "A1", "B1", "B2", "C1", "C2", "CHK"],
            campaigns=campaigns,
        )
        params.update(changes)
        return evaluate_promotions(**params)

    def test_approved_weekly_sale_can_display(self):
        result = self.evaluate([campaign()])
        self.assertEqual([item["campaign_id"] for item in result["eligible_promotions"]], ["CAMPAIGN-001"])

    def test_sponsored_requires_disclosure(self):
        value = campaign(source="sponsored-placement", disclosure={"sponsored": False, "text": ""})
        result = self.evaluate([value])
        self.assertEqual(result["suppressed_promotions"][0]["reason"], "missing-sponsorship-disclosure")

    def test_sponsored_with_disclosure_can_display(self):
        value = campaign(source="sponsored-placement", disclosure={"sponsored": True, "text": "Sponsored"})
        result = self.evaluate([value])
        self.assertEqual(result["eligible_promotions"][0]["source"], "sponsored-placement")

    def test_non_active_states_are_suppressed(self):
        for state in ["draft", "pending-approval", "paused", "rejected", "revoked", "expired"]:
            with self.subTest(state=state):
                result = self.evaluate([campaign(lifecycle_state=state)])
                self.assertFalse(result["eligible_promotions"])

    def test_other_location_is_suppressed(self):
        result = self.evaluate([campaign(location_scope=["OTHER"])])
        self.assertEqual(result["suppressed_promotions"][0]["reason"], "location-out-of-scope")

    def test_outside_corridor_is_suppressed(self):
        result = self.evaluate([campaign()], route_corridor=["ENT", "A1", "B1", "C1", "CHK"])
        self.assertEqual(result["suppressed_promotions"][0]["reason"], "outside-route-corridor")

    def test_promotions_can_be_disabled(self):
        result = self.evaluate([campaign()], promotions_enabled=False)
        self.assertEqual(result["suppressed_promotions"][0]["reason"], "promotions-disabled")

    def test_campaign_id_is_final_tie_breaker(self):
        second = campaign(campaign_id="CAMPAIGN-002")
        first = campaign(campaign_id="CAMPAIGN-001")
        result = self.evaluate([second, first])
        self.assertEqual([item["campaign_id"] for item in result["eligible_promotions"]], ["CAMPAIGN-001", "CAMPAIGN-002"])

    def test_evaluation_is_repeatable(self):
        values = [campaign(), campaign(campaign_id="CAMPAIGN-002")]
        self.assertEqual(self.evaluate(values), self.evaluate(values))

    def test_route_protection_contract(self):
        corridor = ["ENT", "A1", "B1", "B2", "C1", "C2", "CHK"]
        before = canonical_hash(corridor)
        result = self.evaluate([campaign()], route_corridor=corridor)
        self.assertEqual(before, canonical_hash(corridor))
        self.assertFalse(result["route_protection"]["replacement_route_returned"])
        self.assertFalse(result["route_protection"]["route_plan_accepted"])


if __name__ == "__main__":
    unittest.main()

