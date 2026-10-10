"""Hugging Face Space for the public Cortex Spatial Intelligence review demo."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

import gradio as gr

from reference_engine import (
    ReferenceInputError,
    canonical_hash,
    evaluate_promotions,
    load_fixture,
    plan_route,
    plan_stocking,
)


ROOT = Path(__file__).resolve().parent
FIXTURE = load_fixture(ROOT / "fixtures" / "synthetic_store.json")
NODE_CHOICES = [node["id"] for node in FIXTURE["nodes"]]
SKU_CHOICES = [item["sku"] for item in FIXTURE["merchandise"]]


def _error_payload(exc: Exception) -> dict[str, Any]:
    return {
        "status": "rejected",
        "error_type": type(exc).__name__,
        "message": str(exc),
        "implementation": "independent-public-reference",
    }


def _svg_for_path(path: list[str] | None) -> str:
    nodes = {node["id"]: node for node in FIXTURE["nodes"]}
    selected = set(path or [])
    segments: list[str] = []
    for edge in FIXTURE["edges"]:
        a, b = nodes[edge["a"]], nodes[edge["b"]]
        used = False
        if path:
            pairs = set(zip(path, path[1:]))
            used = (edge["a"], edge["b"]) in pairs or (edge["b"], edge["a"]) in pairs
        color = "#2563eb" if used else "#cbd5e1"
        width = 7 if used else 3
        segments.append(
            f'<line x1="{40+a["x"]*65}" y1="{360-a["y"]*48}" '
            f'x2="{40+b["x"]*65}" y2="{360-b["y"]*48}" stroke="{color}" stroke-width="{width}" />'
        )
    points: list[str] = []
    for node_id, node in nodes.items():
        x, y = 40 + node["x"] * 65, 360 - node["y"] * 48
        fill = "#f97316" if node_id in selected else "#0f172a"
        points.append(f'<circle cx="{x}" cy="{y}" r="10" fill="{fill}" />')
        points.append(
            f'<text x="{x+13}" y="{y+5}" font-size="13" fill="#0f172a">{html.escape(node_id)}</text>'
        )
    return (
        '<div class="map-card"><svg viewBox="0 0 620 400" role="img" '
        'aria-label="Synthetic route graph">'
        + "".join(segments + points)
        + "</svg></div>"
    )


def run_route(workflow: str, start: str, skus: list[str], end: str):
    try:
        result = plan_route(FIXTURE, workflow=workflow, start_node=start, skus=skus, end_node=end)
        return result, _svg_for_path(result["full_path"])
    except (ReferenceInputError, TypeError, ValueError) as exc:
        return _error_payload(exc), _svg_for_path(None)


def _parse_lines(value: str) -> list[dict[str, Any]]:
    records = []
    for index, raw in enumerate(value.splitlines()):
        raw = raw.strip()
        if not raw:
            continue
        pieces = [part.strip() for part in raw.split(":")]
        if len(pieces) != 2:
            raise ReferenceInputError("stocking lines must use SKU:quantity")
        records.append({"line_id": f"line-{index+1}", "sku": pieces[0], "quantity": int(pieces[1])})
    return records


def run_stocking(bay: str, sequence: str, lines: str, include_checkout: bool):
    try:
        result = plan_stocking(
            FIXTURE,
            bay_node=bay,
            sequence=sequence,
            line_items=_parse_lines(lines),
            end_node="CHK" if include_checkout else None,
        )
        return result, _svg_for_path(result["full_path"])
    except (ReferenceInputError, TypeError, ValueError) as exc:
        return _error_payload(exc), _svg_for_path(None)


DEFAULT_CAMPAIGNS = json.dumps(
    [
        {
            "campaign_id": "WEEKLY-001",
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
            "disclosure": {"sponsored": False, "text": "Weekly sale"}
        },
        {
            "campaign_id": "SPONSORED-001",
            "source": "sponsored-placement",
            "approval_state": "approved",
            "lifecycle_state": "active",
            "location_scope": ["SYNTHETIC-001"],
            "sku": "SYN-MILK",
            "destination_node": "C2",
            "campaign_start": "2026-10-01T00:00:00Z",
            "campaign_expiration": "2026-11-01T00:00:00Z",
            "placement_tier": 2,
            "proximity_threshold_m": 15,
            "disclosure": {"sponsored": True, "text": "Sponsored placement"}
        }
    ],
    indent=2,
)


def run_promotions(current: str, corridor: str, timestamp: str, campaigns_text: str, enabled: bool):
    try:
        corridor_nodes = [part.strip() for part in corridor.split(",") if part.strip()]
        campaigns = json.loads(campaigns_text)
        route_snapshot = {"corridor": list(corridor_nodes), "sha256": canonical_hash(corridor_nodes)}
        result = evaluate_promotions(
            FIXTURE,
            evaluation_timestamp=timestamp,
            location_id="SYNTHETIC-001",
            current_node=current,
            route_corridor=corridor_nodes,
            campaigns=campaigns,
            promotions_enabled=enabled,
        )
        result["route_snapshot_before"] = route_snapshot
        result["route_snapshot_after"] = {"corridor": list(corridor_nodes), "sha256": canonical_hash(corridor_nodes)}
        result["route_unchanged"] = result["route_snapshot_before"] == result["route_snapshot_after"]
        return result
    except (ReferenceInputError, TypeError, ValueError, json.JSONDecodeError) as exc:
        return _error_payload(exc)


def run_repeatability():
    request = {
        "workflow": "shopper",
        "start_node": "ENT",
        "skus": ["SYN-MILK", "SYN-APPLE", "SYN-CEREAL"],
        "end_node": "CHK",
    }
    outputs = [plan_route(FIXTURE, **request) for _ in range(10)]
    hashes = [canonical_hash(output) for output in outputs]
    return {
        "runs": len(outputs),
        "unique_output_hashes": sorted(set(hashes)),
        "identical": len(set(hashes)) == 1,
        "request": request,
        "note": "This verifies only the independent public reference implementation and synthetic fixture.",
    }


CSS = """
.gradio-container { max-width: 1180px !important; }
.boundary { border-left: 5px solid #f97316; background: #fff7ed; padding: 14px 18px; border-radius: 10px; }
.map-card { background: white; border: 1px solid #cbd5e1; border-radius: 14px; padding: 8px; }
.map-card svg { width: 100%; height: auto; }
"""


with gr.Blocks(css=CSS, title="Cortex Spatial Intelligence — Public Review Lab") as demo:
    gr.Markdown("# Cortex Spatial Intelligence™ — Public Review Lab")
    gr.Markdown(
        """<div class="boundary"><strong>Public disclosure boundary.</strong> This Space is an independently written,
        synthetic reference demonstrator. It contains no production SDK source, customer map, private adapter,
        proprietary optimization implementation, credential, or operational deployment detail. Results from this
        Space demonstrate only the public reference contract under the stated synthetic conditions.</div>"""
    )

    with gr.Tab("Shopper / Picker"):
        with gr.Row():
            workflow = gr.Radio(["shopper", "picker"], value="shopper", label="Workflow")
            start = gr.Dropdown(NODE_CHOICES, value="ENT", label="Start node")
            end = gr.Dropdown(NODE_CHOICES, value="CHK", label="End node")
        skus = gr.Dropdown(SKU_CHOICES, value=["SYN-MILK", "SYN-APPLE", "SYN-CEREAL"], multiselect=True, label="Synthetic merchandise list")
        route_button = gr.Button("Plan deterministic route", variant="primary")
        with gr.Row():
            route_json = gr.JSON(label="Ordered route and evidence")
            route_map = gr.HTML(value=_svg_for_path(None), label="Synthetic map")
        route_button.click(run_route, [workflow, start, skus, end], [route_json, route_map], api_name="plan_reference_route")

    with gr.Tab("Stocking / Replenishment"):
        with gr.Row():
            bay = gr.Dropdown(NODE_CHOICES, value="BAY", label="Receiving or staging bay")
            sequence = gr.Radio(["closest-first", "farthest-first"], value="closest-first", label="Governed sequence")
            include_checkout = gr.Checkbox(value=False, label="End at checkout")
        lines = gr.Textbox(value="SYN-MILK:4\nSYN-APPLE:2\nSYN-BULK:3\nSYN-CEREAL:1", lines=6, label="Lines (SKU:quantity)")
        stocking_button = gr.Button("Plan stocking work", variant="primary")
        with gr.Row():
            stocking_json = gr.JSON(label="Stocking plan and evidence")
            stocking_map = gr.HTML(value=_svg_for_path(None), label="Synthetic map")
        stocking_button.click(run_stocking, [bay, sequence, lines, include_checkout], [stocking_json, stocking_map], api_name="plan_reference_stocking")

    with gr.Tab("Governed Promotions"):
        gr.Markdown("Promotions are evaluated against an existing corridor. The evaluator receives no RoutePlan and returns no route.")
        with gr.Row():
            current = gr.Dropdown(NODE_CHOICES, value="B1", label="Current synthetic node")
            corridor = gr.Textbox(value="ENT,A1,B1,B2,C1,C2,CHK", label="Existing route corridor")
            timestamp = gr.Textbox(value="2026-10-10T16:00:00Z", label="Explicit UTC evaluation timestamp")
            enabled = gr.Checkbox(value=True, label="Promotions enabled")
        campaigns = gr.Code(value=DEFAULT_CAMPAIGNS, language="json", label="Synthetic campaigns")
        promotion_button = gr.Button("Evaluate promotions without rerouting", variant="primary")
        promotion_json = gr.JSON(label="Eligible and suppressed decisions")
        promotion_button.click(run_promotions, [current, corridor, timestamp, campaigns, enabled], promotion_json, api_name="evaluate_reference_promotions")

    with gr.Tab("Repeatability"):
        gr.Markdown("Run the same request ten times and compare canonical output hashes.")
        repeat_button = gr.Button("Run repeatability check", variant="primary")
        repeat_json = gr.JSON(label="Repeatability evidence")
        repeat_button.click(run_repeatability, outputs=repeat_json, api_name="repeatability_check")

    with gr.Tab("Review scope"):
        gr.Markdown(
            """
## What reviewers can inspect

- Explicit synthetic inputs and outputs.
- Stable deterministic tie-breaking.
- Graph-distance versus coordinate-distance behavior.
- Full path reconstruction.
- Stocking order preservation.
- Promotion lifecycle, disclosure, proximity, and corridor suppression.
- Route protection and repeatability evidence.

## What is not in this Space

- The production TypeScript SDK or private repository history.
- Production route-optimization and policy implementations.
- Real retailer floor plans, merchandise records, positioning histories, or customer data.
- Proprietary adapters, deployment configuration, commercial credentials, or internal evidence.

The public package includes a claims ledger, methodology, limitations, test results, and reviewer guide.
"""
        )


if __name__ == "__main__":
    demo.launch()

