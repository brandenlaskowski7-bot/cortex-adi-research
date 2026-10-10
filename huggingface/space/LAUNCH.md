# Free launch handoff

The owner chose **no subscription**. Use the existing **private Static Space**:

**https://huggingface.co/spaces/BrandenLaskowski7/cortex-governed-memory-challenge**

Hugging Face's creation screen currently requires a paid plan for hosted Gradio/Docker Spaces. CPU Basic's lack of an hourly hardware charge does not remove that subscription requirement. Static Spaces remain free. This preparation uses the free Static option; no subscription or paid compute was purchased.

## What is prepared

- Hugging Face serves the public-safe guide in `huggingface/static-space/`.
- The guide embeds or links to `https://challenge.aiadvantage.shop/demo/`.
- The Gradio client runs on the owner's existing Mac in a separate resource-limited client container. Its source is the public `huggingface/space/` folder. It calls only the fixed documented HTTPS API. No private kernel, credentials, production memory, Docker internals, or evidence ledger are uploaded to Hugging Face or this public repository.
- The isolated synthetic lab enforces 90-minute maximum visits, 15-minute idle expiry, reset without deadline extension, End session, and automatic cleanup. Credentials stay per visitor in the client server's memory. See [lifecycle](../../challenges/governed-memory/LIFECYCLE.md).
- The owner's separate local ON/OFF controls check the reviewed deployment, start/stop only the demo entrance, and revoke/clean lab visits when turned off. Their private implementation stays outside this repository.

The account `BrandenLaskowski7` is authenticated in the owner's browser and the private Space was created and populated through that interface. The connector remains read-only for repositories; no new write token or expanded connector permission was created.

## The one remaining owner decision

**Explicitly approve public activation of the prepared free demo.** For example: “Turn on the free Cortex challenge and make the prepared Space public.” Until that decision, leave the Space private and the public entrance off. A private Space displaying “Running” does not mean the challenge is publicly launched.

After approval, the operator opens the reviewed demo entrance, verifies HTTPS health/capacity, changes this Space to Public, and verifies it while signed out. If a critical check fails, close the entrance and report the failure. Never call it live solely because a Space exists or a build is green.

For an owner doing the final switch manually:

1. Keep the Mac awake, Docker running, and internet connected. The free arrangement depends on these existing resources; it is not free cloud compute or guaranteed uptime.
2. Open the supplied **Turn ON Cortex Challenge** control. It must report verified HTTPS readiness. If it says NOT READY, leave the Space private and ask the operator to inspect the named prerequisite.
3. Sign into Hugging Face and open the Space link above.
4. Open **Settings**, find **Repository visibility**, choose **Change visibility → Public**, and confirm only after reviewing the public-safe files. Public source may be copied permanently.
5. Open the public Space while signed out. Click **Open interactive lab here**, or **Open in a new tab** if embedded cookies are blocked. Run one synthetic scenario, inspect the decision and receipt, then **End session and erase my experiment**.
6. If busy/full, stop and report the capacity limit; do not repeatedly open sessions. If the check fails critically, use **Turn OFF Cortex Challenge**. That closes the entrance, pauses new visits, revokes managed visits, and stops the separate demo client.

## Recreate or restore the free Space

These steps are for recovery, not an additional action needed for the existing Space.

1. Open [New Space](https://huggingface.co/new-space), choose your account and an available name.
2. Choose **Static → Blank**, **CC BY 4.0**, and **Private**. Do not select Gradio, Docker, PRO, a GPU, or paid hardware for this free plan.
3. Create the Space, then open **Files → Contribute → Upload files**.
4. Upload **only** `huggingface/static-space/index.html`, `README.md`, and `LICENSE` directly to the Space root. The README must retain `sdk: static` and `app_file: index.html`.
5. Commit and open **App** to inspect the guide. If upload is unavailable, use the site's file editor to paste those exact file contents.
6. Keep visibility Private until the explicit activation decision above. Never upload the enclosing repository, `.git`, `.venv`, local outputs, private implementation, runtime files, or secrets.

## First developer outreach

After verified public activation, invite three developers who build agent or memory tools to test one invariant each. Share the verified Space URL, API contract, and [synthetic failure template](https://github.com/brandenlaskowski7-bot/cortex-adi-research/issues/new?template=challenge-failure.yml). Ask for expected versus observed decision, reason category, receipt ID, and UTC time; omit credentials and real data. No invitations have been sent.

[Hugging Face Space overview](https://huggingface.co/docs/hub/spaces-overview) · [Static Space documentation](https://huggingface.co/docs/hub/spaces-sdks-static) · [Verification record](VERIFICATION.md)
