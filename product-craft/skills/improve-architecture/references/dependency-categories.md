# Dependency Categories

When assessing a module for deepening, classify each of its dependencies into one of
four categories. The category determines the testing strategy and refactoring approach.

## Category 1: In-Process

Pure computation, in-memory state, no I/O.

**Examples**: parsers, validators, formatters, state machines, calculators,
data transformers, business rule engines.

**Deepening strategy**: Merge the tightly-coupled modules into one deeper module.
Test the merged module directly with unit tests -- no mocking, no substitution needed.

**Testing**: Direct input/output assertions on the public interface.

---

## Category 2: Local-Substitutable

Dependencies that have lightweight local stand-ins usable in tests.

**Examples**: PostgreSQL (via PGLite or embedded Postgres), filesystem
(via in-memory FS or temp directories), SQLite (in-memory mode),
Redis (via embedded alternatives), message queues (via in-memory implementations).

**Deepening strategy**: The deepened module uses the real dependency interface.
Tests run with the local substitute. The substitute must be behaviorally equivalent
for the operations the module uses.

**Testing**: Integration tests with the local stand-in running inside the test
process. Verify through the module's public interface, not the stand-in's state.

**Validation**: Confirm the local substitute exists and covers the operations used.
If it only covers 80% of operations, the remaining 20% may need a thin
integration test against the real dependency.

---

## Category 3: Ports and Adapters (Remote but Owned)

Services across a network boundary that the team owns (microservices, internal APIs,
internal queues).

**Examples**: internal REST/gRPC APIs, internal message bus consumers, internal
storage services, internal auth services.

**Deepening strategy**: Define a port (interface) at the module boundary. The deep
module owns the business logic; transport is injected. Implement two adapters:
a production adapter (HTTP/gRPC/queue) and an in-memory test adapter.

**Testing**: Unit tests use the in-memory adapter. The module under test never
knows whether it is talking to a real service or a test double. A separate thin
integration test verifies the production adapter against the real service.

**Interface design**: The port should express domain operations ("place order",
"check inventory"), not transport operations ("POST /orders", "GET /stock/:id").
This keeps the module's logic decoupled from wire protocol changes.

---

## Category 4: True External (Mock at Boundary)

Third-party services the team does not control.

**Examples**: Stripe, Twilio, SendGrid, AWS S3, external OAuth providers,
third-party analytics APIs.

**Deepening strategy**: The deepened module takes the external dependency as
an injected port. Tests provide a mock implementation. Production provides
the real client.

**Testing**: Mock at the boundary only. The mock implements the same port
interface as the real client. Test the module's logic exhaustively through
its public interface with the mock injected. A separate contract test
(or smoke test) verifies the real client against the external service.

**Boundary rule**: Never mock deeper than the immediate boundary. If module A
calls module B which calls Stripe, mock Stripe in module B's tests, not in
module A's tests. Module A tests with the real module B (or its in-memory
adapter if B is a port).

---

## Selection Flowchart

```
Does the dependency involve I/O?
  NO  --> Category 1: In-Process (merge and test directly)
  YES --> Is there a local stand-in?
            YES --> Category 2: Local-Substitutable (test with stand-in)
            NO  --> Do we own the remote service?
                      YES --> Category 3: Ports & Adapters (define port, inject adapter)
                      NO  --> Category 4: True External (mock at boundary)
```
