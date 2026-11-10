# Portal extensions catalogue

The list of extensions that Portal shows under **Settings, Extensions, Browse extensions** and at
<https://getportaltv.net/extensions/>.

Being listed means someone read the entry and checked its source link. **It is not a security audit.** Extensions are other
people's apps and are not covered by Portal's no-ads, no-tracking promise.

## How it works

- One file per extension in `entries/`, named `<package>.json` (for example `entries/net.example.garage.json`).
- `revoked.json` is a list of lines that switch an extension off wherever it is installed.
- `scripts/build-catalog.py` joins them into `catalog.json`. The maintainer then stamps and **signs** it offline and publishes
  it with `catalog.json.sig` to `site/extensions/` in [plecos/portaltv](https://github.com/plecos/portaltv). Portal refuses a
  catalog that isn't signed by its key, so a pull request here can never put an app on a TV by itself.
- Authors host their own APKs. The catalogue holds a link and a checksum, never the file.

The format of an entry, the revoked list, and the checks Portal makes before installing are in
[docs/CATALOG.md](https://github.com/plecos/portaltv/blob/main/docs/CATALOG.md). How to write an extension:
[quickstart](https://github.com/plecos/portaltv/blob/main/docs/EXTENSIONS-QUICKSTART.md).

## Listing your extension

1. Build and host a release APK over https. Note its size and SHA-256 (`shasum -a 256 app.apk`) and its signer
   (`apksigner verify --print-certs app.apk`, the SHA-256 digest of the certificate).
2. Copy `entries/example.json.txt` to `entries/<your.package>.json` and fill it in. Every field is explained in
   `docs/CATALOG.md`.
3. Open a pull request. CI builds the catalogue and checks it with the same parser Portal uses, and downloads your APK to check
   its checksum. Fix whatever it says.
4. A reviewer goes through the checklist in the pull request. When it is merged, the maintainer signs and publishes the next
   catalogue. That can take a few days.

To **update** an extension, add a new item to its `versions` (keep the old ones unless they are unsafe). To **withdraw** one, add
a line to `revoked.json`; the reason is shown to people who have it installed.

## For the maintainer

Publishing is manual on purpose; the signing key never goes in CI.

```bash
git clone https://github.com/plecos/portaltv     # next to this repo
python3 scripts/build-catalog.py build/catalog.json
cp ../portaltv/site/extensions/catalog.json build/previous.json    # to carry the serial forward
java ../portaltv/scripts/CatalogSign.java stamp build/catalog.json --serial $(( $(grep -o '"serial": *[0-9]*' build/previous.json | grep -o '[0-9]*$') + 1 ))
../portaltv/scripts/validate-catalog.sh "$PWD/build/catalog.json"
java ../portaltv/scripts/CatalogSign.java sign ~/portal-catalog-keys/portal-catalog.private portal-catalog-1 build/catalog.json
cp build/catalog.json build/catalog.json.sig ../portaltv/site/extensions/     # then a pull request in plecos/portaltv
```

The catalogue is good for 180 days from the stamp. Publish again before it expires or Browse stops installing.
