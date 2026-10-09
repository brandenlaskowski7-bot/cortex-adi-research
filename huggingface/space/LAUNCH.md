# Owner launch handoff

Status: **prepared on GitHub; not created, published, or verified on Hugging Face**.

The connected account is `BrandenLaskowski7`. The connector grants profile/read scopes and jobs access, but **no repository write/create scope**. There is no local Hugging Face credential. No permission was expanded, no token was requested or copied, and no Space creation was attempted with insufficient authority.

The remaining owner handoff is to create and upload this Space in the Hugging Face UI, then explicitly authorize public go-live after private verification. No secret is needed to run it.

## Click-by-click creation

1. Sign into [Hugging Face](https://huggingface.co) as **BrandenLaskowski7**.
2. Open [Create a new Space](https://huggingface.co/new-space).
3. Select owner **BrandenLaskowski7**. Enter Space name **cortex-governed-memory-challenge**. If it already exists, inspect it; do not overwrite an unrelated Space.
4. Enter short description **Six synthetic memory experiments with decisions and receipts**.
5. Choose **CC BY 4.0** as license, **Gradio** as SDK, **Blank** template if offered, and free **CPU Basic** hardware. No GPU or paid hardware is required.
6. Select **Private** visibility for review, then click **Create Space**. Private staging is the intended initial state; do not choose Public at this step.
7. In **Files**, choose **Add file → Upload files**. Upload the files below directly to the Space root, preserving the `tests/` subfolder if including tests. Do **not** upload the enclosing GitHub repository or any `.git`, `.venv`, cache, token, or local output folder.
8. Commit the upload to the private Space. Wait for the build to finish. Open **App**, or open its app URL in a separate tab if your browser blocks iframe cookies.
9. Confirm the six scenario names and limitations are visible. Run **Temporal expiry**, verify the receipt, and reset that same session. Check that the trace reports matched decisions. This uses one finite API session slot. Stop if the endpoint returns capacity/unavailability; do not repeatedly create visitors.
10. Review the source and private result. Give explicit owner confirmation: **“Go live with BrandenLaskowski7/cortex-governed-memory-challenge using the reviewed GitHub commit.”** Public publication is still pending until that confirmation.
11. After confirming, open **Settings → Repository visibility → Change visibility → Public** and accept the site's confirmation. Public source may be copied permanently. Publish only the allowlisted client files.
12. Open the public Space while signed out, verify the app loads, and perform one bounded synthetic scenario/receipt/reset if capacity permits. If capacity is full, report **published, live interaction blocked by capacity**, not verified live. Record the actual Space URL, Hugging Face revision, timestamp, and observed result in the GitHub docs. Do not claim hosted verification from the local tests.

Expected URL **if created with that owner/name**: `https://huggingface.co/spaces/BrandenLaskowski7/cortex-governed-memory-challenge`. This is a proposed destination, not an existing/live resource verified by this preparation.

## Upload allowlist

Required at Space root:

- `app.py`
- `challenge.py`
- `scenarios.py`
- `requirements.txt`
- `README.md`
- `LICENSE`
- `LAUNCH.md`
- `VERIFICATION.md`

Optional, preserving paths: `tests/test_client.py`, `tests/test_boundary.py`, `tests/live_smoke.py`.

No fixture dataset publication is required for this Space. Existing `huggingface/fixtures.jsonl` and its dataset card are separate preparation and should not replace this Space README.

For a future authorized CLI uploader, authenticate using the normal Hugging Face flow, then create a **private** Gradio Space and upload **only this folder** with the allowlist above. Never paste a token into chat, source, a command argument, or a screenshot.

## Before outreach

Coordinate a small first cohort (for example, three developers) because the upstream 32-slot limit has no automatic reclamation. The documented public API cannot report available slots or reclaim them. Do not change production or invent a session-recycling mechanism in this client. Have the challenge owner confirm lab capacity through their existing authorized operations process.

After public hosted verification, invite developers to choose one invariant, run a synthetic scenario, and report the expected versus observed decision, reason category, receipt ID, and UTC time through the GitHub failure template. Ask them to omit credentials and real data. The first practical outreach step is a small invitation to three agent/memory-tool developers, with the verified Space link, contract, and a request to find a counterexample. No invitation has been sent.

Reference: [Hugging Face Gradio Space creation guide](https://huggingface.co/docs/hub/spaces-sdks-gradio).
