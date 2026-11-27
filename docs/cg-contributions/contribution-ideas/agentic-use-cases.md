# Agentic use cases

Contribution candidate for the [Use cases and requirements draft](../../knowledge-base/atag-cg/ucr.md): specific agentic creator and consumer use cases, with the wording each one would need. The feedback received on the idea was that specific examples would be useful.

The position below is that an agent is not a fourth user role. It is software acting on behalf of a person who already holds one of the three existing roles. That keeps the draft's user model and puts the new requirement burden where it belongs, on the authoring tool.

## Agents sit in the existing stack

An agent can be deployed in any of three places relative to ATAG's subject, the authoring tool. In each case the human behind it is the actor for ATAG's purposes.

| Placement                    | Who the agent works for   | ATAG relevance                                                                                                 |
| ---------------------------- | ------------------------- | -------------------------------------------------------------------------------------------------------------- |
| Inside the authoring tool    | The creator or maintainer | The tool's own agent features are the tool's interface, so the draft's requirements apply to them as they are. |
| Alongside the authoring tool | The creator or maintainer | The agent drives the tool through an API, MCP server, or headless endpoint rather than a user interface.       |
| Inside the user agent        | The consumer              | Consumption, not authoring. Relevant to ATAG only where the consumer is also handed an authoring surface.      |

The group already leans this way. Recorded in the [9 October 2026 minutes](https://w3c-cg.github.io/atag/minutes/minutes_Oct09_2026), read out by Ned Zimmerman from the chat: "even autonomous, quote-unquote, autonomous AI agents have a human user deploying them. I would call that human as filling the applicable role." Wendy Reid raised the same question on 17 July 2026 ("Does an LLM rise to the level of a role?") and Hidde de Vries answered that non-human roles are possible. Charles Hall's framing on 9 October: "ATAG only cares about the human part of these cases."

Where the group has not settled anything is the second row. An agent driving a tool through an API has no authoring interface for ATAG to make accessible, and the draft has no requirements written for that path, even though the [charter](https://w3c-cg.github.io/atag/ATAG_Charter.html) names "API-driven, headless, and web-based platforms" as a development the group is to explore.

## Why the current draft cannot absorb these use cases

Three constraints, all visible in the published draft and all structural rather than editorial.

**Use cases start from a human subject.** All eight use cases open with "Users", seven of them as "Users must be able to…", and the user types are defined as people: creator, maintainer, consumer. A tool-facing use case needs a subject like "an agent acting for a creator". That is a wording change across the use cases plus the requirements that mirror them, not an added section.

**The functions list is not wired to anything.** Eight of the 15 named functions never appear again in the draft: diagram editing, voice editing, collaborative editing, version control, annotations and comments, content templates, generative AI or LLM interfaces, and content previews. Two more, rich text and translation, appear only in requirements. So "Generative AI or LLM interfaces" is currently a function with no use case and no requirement, which is exactly the gap this contribution fills.

**The requirements assume a person reading a message.** The tool accessibility requirements cover "interface, features, and documentation", the validation group asks the tool to provide "the necessary information for the user to address any identified issues", and the three places that mention informing the user all mean a human at a screen. Nothing covers returning a machine-readable result, so a tool that reports a pass to an agent has no requirement to report anything true. The draft also never uses cost, token, warning, undo, confirmation, or workflow, all of which came up in the review of ATAG 2.0.

## Candidate use cases

Each row is a specific scenario, the draft section it would sit in, and the requirement it implies. The scenarios come from CMS agent readiness work: exposing a CMS's content model to agents, and deciding what the agent is allowed to do on its own.

| #   | Scenario                                                                                               | Draft section                   | Requirement it implies                                                                                        |
| --- | ------------------------------------------------------------------------------------------------------ | ------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| 1   | A maintainer asks an agent to add alternative text to 40 existing images in a CMS.                     | Modification: metadata          | The tool must expose alternative text requirements to an agent, and reject or flag a submission without them. |
| 2   | A creator asks an agent to build a page from a template, and the agent chooses heading levels.         | Creation: control over creation | The tool must apply its accessible template structure when content arrives programmatically, not only by UI.  |
| 3   | An agent writes content into a headless CMS with no editing interface anyone sees.                     | Creation: technical content     | Requirements must be satisfiable by a tool whose only interface is an API.                                    |
| 4   | A creator reviews agent-generated content before publication and must be able to check it.             | Modification: editing           | The review surface must be accessible, and must show which accessibility features the agent applied.          |
| 5   | An agent runs for 20 minutes, spends money, and produces partial output before the person can stop it. | Not covered                     | Warnings before costly or irreversible steps, with configurable thresholds and an interruptible run.          |
| 6   | A consumer uses an agent to read content on their behalf, and the agent misreads the structure.        | Not covered                     | Content must carry the structure its authoring tool had available, so consumer-side agents are not guessing.  |

Use cases 1 to 4 stay inside ATAG. Use case 5 was discussed in the ATAG 2.0 review as a new "communication of cost or change" area ([5 June 2026](https://w3c-cg.github.io/atag/minutes/minutes_Jun05_2026)) and is not in the draft. Use case 6 is the boundary case: ATAG's leverage is upstream, on the structure the tool emits, not on the consumer agent.

### The confirmation gate

The single mechanism that makes 1 to 5 tractable is the confirmation setting Wendy Reid described on 17 July 2026: an agent that "has to ask me permission before it does anything" versus one that runs "in auto mode". That setting is where an authoring tool's existing accessibility features either reach the human or do not.

The person delegates a task to an agent, which either acts with confirmation or acts and notifies afterwards. In both cases the tool returns accessibility prompts and validation results to the agent, and emits content that carries its accessibility features. Where a person is expected to verify output, the tool also has to present a review surface; where it is not, the notifications are the only record. Separate from that loop, a consumer's agent reads the published content on the consumer's behalf.

Both branches are legitimate. What ATAG can require is that the confirming path is accessible, that the review surface exists when a person is expected to verify output, and that the notifying path reports what was done in a form the person can check.

## Requirements the draft is missing

Four additions that follow from the table above, phrased to fit the existing groups.

- **Machine-readable results.** Under _authoring tool validation_: the tool must be able to report evaluation results and required inputs in a machine-readable form, not only through its interface. This covers both an agent driving the tool and an agent reading the tool's report.
- **Agent-facing feature discovery.** Under _authoring tool accessibility_: the tool must be able to describe its accessible-content-support features and requirements to a program acting for the user. Without this, an agent cannot know that a tool needs alternative text before it saves, and will discover it only by failing validation.
- **Control over agent actions.** Under _authoring accessible content_: the tool must let the person configure which authoring actions an agent may take without confirmation, and make the difference between confirmed and unconfirmed changes visible afterwards.
- **Structure preservation for downstream consumers.** Under _authoring tool outputs_: the tool must preserve structure that its own interface relies on, so that the content remains interpretable by software reading it later. This is the one place where the consumer role earns a requirement rather than a definition.

## Open questions for the group

- Is "an agent acting for a creator" an acceptable use case subject, or does the document stay with human subjects and state the delegation in a note?
- Does the group adopt job stories, which dissolve the question by dropping the role? A candidate wording: "When I am creating content through an agent, I want the tool to tell the agent what accessibility information is required, so I can publish without checking every field." Job stories were proposed on 2 October 2026 and are still listed as open.
- Do agent-driven writes belong to the creator or the maintainer? The distinction is already contested for humans.
- Where does responsibility sit when a tool's agent feature calls a third-party model? This is the responsibility-chain question, raised repeatedly since 9 October 2026 and still unowned.
- Should agent-facing requirements be normative, given that a headless tool cannot meet the interface ones?

## Sources

- [Use Cases and Requirements](https://w3c-cg.github.io/atag/docs/ucr/) draft, as published; wording checked on 19 November 2026.
- [13 November 2026](https://w3c-cg.github.io/atag/minutes/minutes_Nov13_2026): Charles Hall on AI authoring "on behalf of the user on behalf of the author", and Mitchell Evan asking reviewers to record which kind of tool they had in mind.
- [9 October 2026](https://w3c-cg.github.io/atag/minutes/minutes_Oct09_2026): Jutta Treviranus proposing "agent editing" as a use case, the human-behind-the-agent position, and the responsibility chain discussion.
- [17 July 2026](https://w3c-cg.github.io/atag/minutes/minutes_Jul17_2026): whether an LLM has a role, and agent permission settings.
- [5 June 2026](https://w3c-cg.github.io/atag/minutes/minutes_Jun05_2026): token cost warnings, hard stops, and workflow transparency.
- [2 October 2026](https://w3c-cg.github.io/atag/minutes/minutes_Oct02_2026): agents outside the user agent, and job stories as a format.
- [8 May 2026](https://w3c-cg.github.io/atag/minutes/minutes_May08_2026): agent skills, MCP, and the idea of an "ATAG MCP".
- [11 September 2026](https://w3c-cg.github.io/atag/minutes/minutes_Sep11_2026): WebMCP mentioned as a W3C technology for agents to interface with.
- [ATAG#12], [ATAG#15], and [ATAG#37] for the tool taxonomy, the use case thread, and the request for machine-checkable success criteria.
- [ATAG CG](../../knowledge-base/atag-cg/README.md) for the charter, which names API-driven and headless platforms.
