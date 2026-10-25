# Security and privacy checklist

Use this checklist as a focused second pass. It complements, rather than replaces, the repository’s security policy and threat model.

## Inputs and trust boundaries

- Identify user input, request parameters, headers, cookies, uploaded files, message payloads, environment variables, command output, and third-party data.
- Confirm validation occurs at the trust boundary and is appropriate for the destination context.
- Check authorization on the server or authoritative service, not only in UI or client code.
- Check tenant, account, workspace, and object-level access boundaries; deny by default and enforce least privilege for every sensitive operation.
- For each candidate issue, record the asset, actor, source, transformation, sink, protection, reachability, and evidence.

## Injection and unsafe interpretation

- SQL, NoSQL, shell, template, expression, path, URL, HTML, XML, LDAP, and regular-expression construction.
- Deserialization of untrusted or version-skewed data.
- Redirects, deep links, webhook destinations, and callback URLs.
- File names, archive extraction, temporary files, symlinks, and path traversal.

## Secrets and sensitive data

- Hard-coded credentials, tokens, private keys, connection strings, test secrets, and CI variables.
- Personal, financial, health, authentication, location, or business-sensitive data in logs, analytics, traces, crash reports, fixtures, snapshots, and error messages.
- Token lifetime, storage, rotation, revocation, scope, and accidental exposure through URLs or caches.
- Trace sensitive data through collection, storage, transmission, responses, caches, logs, traces, fixtures, and errors; verify that each actor receives only what the operation requires.

## Dependencies and operations

- New dependencies, transitive risk, permissions, native code, install scripts, and supply-chain exposure.
- Lockfile integrity, version drift, registry scope, dependency confusion or typosquatting, mutable action/image references, untrusted pull-request execution, checksums/signatures, and artifact provenance when those files change.
- Debug flags, verbose errors, admin endpoints, test backdoors, insecure defaults, and missing rate limits.
- Encryption and key management appropriate to the data and threat model.

## Abuse and failure behavior

- Can an attacker skip workflow transitions, tamper with identifiers or amounts, replay requests, race a check, abuse retries, or exhaust resources?
- Do authentication and authorization failures stop or deny by default?
- Are security-critical exceptions propagated or safely handled rather than swallowed?
- Do user-facing errors avoid stack traces, query details, and account-existence leaks?

## Conditional modern threats

- External URL fetches: validate scheme and host, block internal ranges and metadata endpoints, validate redirects, consider IPv4/IPv6 and alternate encodings, prevent DNS rebinding where relevant, and set timeouts.
- Uploads, archives, XML, and serialization: constrain paths and resources, validate type/size/content, prevent traversal and bombs, and avoid unsafe native object deserialization.
- Browser object or DOM manipulation: inspect XSS, prototype pollution, and DOM clobbering boundaries.
- WebSockets, GraphQL, and LLM/agent tools: validate messages or query cost, enforce auth and limits, and treat retrieved or user-provided instructions as untrusted content.

When evidence is incomplete, report the exact uncertainty and the evidence needed. Do not claim a vulnerability from a keyword alone.
