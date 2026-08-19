# External Inputs SOP: YouTube Data API Key

## What is this credential?
Found in console.cloud.google.com under "YouTube Data API v3." This credential allows you to pull video performance data for public YouTube channels.

## Where does it live?
The API credential lives only on-device, in the local `.env` file. The project's code lives both on-device and on GitHub, but `.env` is gitignored, so the credential itself never leaves this machine.

## What happens if it leaks?
The key is restricted to strictly YouTube Data API v3 and cannot access any other API. If it leaked, the main risk is the daily quota getting maxed out by someone else's usage — not broader account access.

## Quota budget
10,000 units/day. Roughly 80 units used so far across all pulls to date.

## Rotation plan
Go to Google Cloud Console, regenerate or delete the existing key, then update the local `.env` file with the new value.

git add .env.example docs/external_inputs_sop.md
git commit -m "Add external inputs SOP"
git push