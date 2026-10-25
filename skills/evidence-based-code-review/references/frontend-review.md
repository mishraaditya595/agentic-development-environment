# Frontend and accessibility review adapter

Use this reference when the change affects rendered UI, components, forms, navigation, browser storage or URL state, client queries, localization, or user interaction.

## Rendered semantics and accessibility

- Inspect the final composed semantics, not only source attributes.
- Verify computed accessible names and descriptions, keyboard reachability, visible focus, focus order, and focus continuity through loading, error, dismissal, and navigation.
- Check form ownership, labels, validation association, submission behavior, overlays, escape/dismissal, and reachability of essential content.
- Consider localization, long text, right-to-left layout, zoom, forced colors/high contrast, reduced motion, and responsive viewports.
- Treat an accessibility failure affecting an essential workflow as a correctness issue, not merely polish.

## State and data ownership

- Trace loading, empty, missing-data, error, retry, optimistic, and disabled states.
- Identify the owner and lifetime of component, URL, browser-storage, cache, and server state.
- Check query keys, invalidation, retry policy, stale data, generated client/schema readiness, and authoritative server-side authorization.
- Check SSR/dehydration or hydration behavior when the framework uses it.

## Components and performance

- Reuse repository primitives and preserve their contracts.
- Check controlled/uncontrolled state, prop ownership, effects, navigation, portals, dismissal, and cleanup.
- Look for unnecessary renders, subscriptions, serialized independent requests, large bundles, and unbounded client work only when a concrete workload is affected.

## Tests

- Prefer semantic user-facing queries and behavior/contract assertions.
- Avoid tests that only assert private implementation details, cosmetic classes, hook/effect structure, or mocked-away behavior.
