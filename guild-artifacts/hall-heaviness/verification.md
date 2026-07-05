# Hall Heaviness Verification

Before screenshots: `guild-artifacts/hall-heaviness/before/`
After screenshots: `guild-artifacts/hall-heaviness/after/`
Side-by-side comparisons: `guild-artifacts/hall-heaviness/compare/`
Metrics: `guild-artifacts/hall-heaviness/metrics/`

## Dominant Fixes

- Runner controls collapsed from a full-width band into the top-bar `Runner` disclosure.
- Per-card model override, queue, why, and cost moved into card details.
- Needs-you now exposes one recommended run by default; secondary runs and specialist rosters are reachable through disclosure.
- Card styling was flattened: lighter borders, smaller radius, no shadow stack.

## Needs-you Metrics

| width | controls before -> after | type sizes before -> after | colors before -> after | scroll vh before -> after |
|---:|---:|---:|---:|---:|
| 360 | 17 -> 12 | 7 -> 6 | 12 -> 11 | 5.83 -> 1.44 |
| 768 | 20 -> 16 | 9 -> 6 | 15 -> 12 | 4.09 -> 1.11 |
| 1440 | 29 -> 19 | 9 -> 6 | 15 -> 12 | 2.12 -> 1 |

## Notes

- Before metrics were captured from the live Hall before this redesign; after metrics were captured from the restarted edited Hall with URL assertions.
- Hidden content inside closed disclosures is excluded from after metrics to match visible screenshot reality.
- The final mobile color drop comes from reusing the existing dark ink token on ember buttons instead of introducing a separate button text color.
- No runner semantics, routes, or command availability were changed; reachability was checked in the live DOM.
