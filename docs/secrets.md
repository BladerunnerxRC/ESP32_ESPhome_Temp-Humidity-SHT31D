# Local credentials

Before pulling this change into another checkout, securely back up its
`secrets.yaml` outside the repository: Git removes previously tracked files when
applying their deletion. Restore that local file after pulling. This development
checkout retained its existing local file when it was untracked.

For a new installation, copy `secrets.example.yaml` to `secrets.yaml` and replace
all example values. Keep the existing API key for an existing device and Home
Assistant integration. Never flash the example key or validation firmware.

Untracking does not erase credentials from Git history. If historical values were
real credentials exposed to others, rotate them through a coordinated device and
Home Assistant migration. This PR does not rotate keys or rewrite history.
