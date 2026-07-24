# Telegram Agent Identity and Evidence-Scope Contract

status: current
authority: owner-confirmed
scope: Telegram bot identity, ownership, intake topology, and AI reasoning

## Canonical identity ownership

### Earesmes

- Earesmes is the primary AIRO assistant and orchestrator persona.
- Hermes is the local WSL runtime underneath Earesmes.
- Earesmes uses its existing dedicated Earesmes Telegram bot.
- The Earesmes bot is not the Arfin bot.
- Its canonical intake is the local persistent gateway acting as the sole
  getUpdates consumer for the Earesmes token.

### Arfin / AIRO Finance

- Arfin is the dedicated AIRO Finance persona.
- Arfin uses its existing dedicated Arfin Telegram bot.
- The Arfin bot is not the Earesmes bot.
- Arfin remains direct and independent until the Owner activates a different
  orchestration model.
- Its credentials may reside in Apps Script Script Properties, Cloudflare
  Worker secrets, or another approved production secret store.

### EarnsAI

- EarnsAI uses its existing dedicated EarnsAI Telegram bot.
- Its bot identity and runtime are independent from Earesmes and Arfin.

## Evidence-scope rule

Every bot, token, webhook, process, and configuration audit must declare the
scope it actually inspected.

A local WSL filesystem scan proves only what was found in the scanned local
paths. It does not prove the presence or absence of credentials in production
secret stores, Apps Script, Cloudflare, BotFather, another machine, or any
unscanned location.

Forbidden inference:

not found in local WSL files -> does not exist in the AIRO ecosystem

Permitted conclusion:

not found within the declared local WSL scan scope

## Fail-closed identity rule

Before recommending any bot creation, token rotation, webhook deletion,
webhook reassignment, polling change, or cross-agent routing change, the AI
operator must truthfully establish:

- the identity contract was read;
- Earesmes and Arfin ownership were resolved;
- the evidence scope was declared;
- local absence was not treated as global absence;
- production secret scope is verified or explicitly unknown;
- the Owner architecture decision was read.
- explicit Owner approval is required for every bot-identity architecture change.

If these conditions are incomplete:

- mutation is not allowed;
- new-bot recommendations are not allowed;
- token-rotation recommendations are not allowed;
- webhook mutation recommendations are not allowed;
- the next action is read-only attribution.

## Mandatory visible response receipt

Every substantive Telegram architecture response must emit one of the following
receipts before giving a technical conclusion, recommendation, command, or
mutation plan.

PASS receipt:

AIRO_AGENT_IDENTITY_GUARD=PASS
IDENTITY_CONTRACT_READ=YES
EARESMES_BOT_OWNERSHIP=RESOLVED
ARFIN_BOT_OWNERSHIP=RESOLVED
EARNSAI_BOT_OWNERSHIP=RESOLVED_OR_NOT_RELEVANT
EVIDENCE_SCOPE_DECLARED=YES
LOCAL_ABSENCE_USED_AS_GLOBAL_ABSENCE=NO
PRODUCTION_SECRET_SCOPE_STATUS=VERIFIED_OR_EXPLICITLY_UNKNOWN
OWNER_ARCHITECTURE_DECISION_READ=YES
NEW_BOT_RECOMMENDATION_ALLOWED=NO
TOKEN_ROTATION_RECOMMENDATION_ALLOWED=NO
WEBHOOK_MUTATION_ALLOWED=NO
MUTATION_ALLOWED=ONLY_WITH_SEPARATE_OWNER_APPROVAL

FAIL receipt:

AIRO_AGENT_IDENTITY_GUARD=FAIL
MUTATION_ALLOWED=NO
NEW_BOT_RECOMMENDATION_ALLOWED=NO
TOKEN_ROTATION_RECOMMENDATION_ALLOWED=NO
WEBHOOK_MUTATION_ALLOWED=NO
NEXT=COMPLETE_IDENTITY_AND_SECRET_SCOPE_ATTRIBUTION

The operator must not claim PASS when any required ownership or evidence-scope
field remains unresolved.

## Prohibited unsupported conclusions

An AI operator must not infer from incomplete inventory:

- that Arfin has no existing bot;
- that Earesmes and Arfin intentionally share one bot;
- that a new Arfin or Earesmes bot must be created;
- that a token must be rotated;
- that the Earesmes and Arfin runtimes should be merged.

A bot bound to the wrong webhook is a binding or routing incident. It is not
evidence that another agent lacks its own bot.

## Current incident classification

The Earesmes-targeted message processed by Arfin must be classified as:

EARESMES_BOT_MISBOUND_TO_ARFIN_WEBHOOK_OR_ROUTING_PATH

It must not be classified as a requirement to create a new bot.
