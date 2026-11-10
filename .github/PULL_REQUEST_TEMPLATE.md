## What this changes

<!-- Adding, updating or withdrawing which extension? -->

## Checklist (the reviewer ticks these, you answer them)

- [ ] **Source link:** the entry's `source` opens the real source, and the APK listed was built from it (or the author says why not).
- [ ] **Licence:** the `license` field says what the source says.
- [ ] **What it asks for:** `capabilities` lists everything its manifest declares, and each one makes sense for what it does.
- [ ] **Signer:** `signer` is the SHA-256 of the APK's signing certificate (`apksigner verify --print-certs app.apk`). For a Google Play entry it is the Play app signing key, not the upload key.
- [ ] **Checksum:** `sha256` and `size` match the file at `apk` (CI checks this).
- [ ] **Names:** nothing in the name, description or package could pass for Portal, Android, Google or a system screen, unless the signer is in Portal's `first-party-signers.txt`.
- [ ] **Honest description:** it says what the extension does, and for a paid one what the free version does and what the paid one adds.
- [ ] **Play entries only:** the Play page exists, belongs to this package, and the `price` matches it.
- [ ] **One thing per pull request,** and the file name is `entries/<package>.json`.

Being listed is a review of the entry, not a security audit. Don't tick a box you haven't checked.
