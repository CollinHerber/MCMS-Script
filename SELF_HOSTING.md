# Self-hosting this marketplace fork

The active MCSManager deployment mounts this repository read-only into the web container:

```text
D:\MCS\Source\MCMS-Script
  -> /opt/mcsmanager/web/public/upload_files/self-hosted-market
```

The panel marketplace source is:

```text
public/upload_files/self-hosted-market/market-v2.json
```

This avoids `script.mcsmanager.com` for marketplace metadata and makes changes to this fork available without rebuilding the MCSManager images.

## Validate changes

```bash
python scripts/validate_market.py
```

The validator fails on malformed JSON or insecure `http://` image URLs. It reports remaining `githubyumao/*` game-runtime image references as warnings so they can be migrated deliberately rather than accidentally.

## What is local and what is not

Local:

- `market-v2.json`, `market.json`, and template metadata.
- Any artwork or downloadable files committed to this repository and referenced with a URL served by the panel or another owned host.

Still external by default:

- `githubyumao/steam-game-runtime` and other Docker images referenced by templates.
- Minecraft/Steam/game vendor downloads.
- Artwork hosted on MCSManager OSS/CDN or third-party sites.
- Setup scripts that download releases from the upstream `MCSManager/MCSManager` repository.

The Docker runtime images can be migrated later by building owned equivalents and replacing each template's `setupInfo.docker.image` and `updateCommandImage` values. External game-vendor downloads generally remain necessary unless licensing permits a mirror.

## Updating from upstream

```bash
git fetch upstream
git checkout master
git merge upstream/master
python scripts/validate_market.py
```

Review upstream URL and image changes before merging them into production.
