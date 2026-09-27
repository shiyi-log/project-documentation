# Pressure scenarios

These scenarios test whether the skill routes documentation proportionately without forcing a route, ledger, workflow, or progress file.

1. **Tiny CLI / time pressure** — `sharkdp/fd`: add one flag and update the user-facing documentation. Do not invent enterprise governance.
2. **Mature library / release pressure** — `psf/requests`: change public API behavior and prepare release documentation. Find API, compatibility, migration, and changelog surfaces.
3. **Multi-service / data risk** — `immich-app/immich`: change a database field and service boundary. Identify migration, contract, deployment, rollback, and operator-doc implications.
4. **Large platform / external authority** — `kubernetes/kubernetes`: update build documentation after a core change. Distinguish repository files from external authoritative docs and platform validation.
5. **Ambiguous scope / authority pressure** — user says “document everything”. Ask for audience and boundary, then propose a bounded inventory.
6. **Trivial edit / anti-overreach** — change one README sentence. Make the smallest valid diff; do not create a route map, ledger, or progress system.

For each scenario, score document scope, route explanation, optional coordination, evidence labels, failure/recovery coverage, and no-side-effect behavior.
