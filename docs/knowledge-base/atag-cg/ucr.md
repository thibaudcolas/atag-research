# Use cases and requirements draft

The group's main deliverable is a [Use Cases and Requirements](https://w3c-cg.github.io/atag/docs/ucr/) document: "a document that we can use as our foundational set of use cases and requirements" (Wendy Reid, [25 September 2026](https://w3c-cg.github.io/atag/minutes/minutes_Sep25_2026)). The [first draft][ATAG#34] was published in October 2026 from the `atag-ucr` branch, structured by authoring actions ([2 October 2026](https://w3c-cg.github.io/atag/minutes/minutes_Oct02_2026)).

## Contents

| Section                  | Contents                                                                                                             |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------- |
| Introduction             | Heading only, no text.                                                                                               |
| User types               | Creator (originator), maintainer (modifies or maintains), and consumer (end user of the result).                     |
| Authoring tool functions | 15 functions, each on a spectrum from the most basic to the most advanced implementation.                            |
| Use cases: creation      | Media content, technical content, and control over content creation.                                                 |
| Use cases: modification  | Editing content, adding accessibility metadata, and exporting content.                                               |
| Use cases: validation    | Checking accessibility, and repairing issues.                                                                        |
| Requirements             | 23 statements in four groups: tool accessibility (6), authoring accessible content (7), validation (4), outputs (6). |

The functions run from rich text, audio, video, image, diagram, voice, programming, and VR/XR/3D CAD editing interfaces, through collaborative editing, version control, annotations, and templates, to generative AI or LLM interfaces, previews, and translation. The list is not wired to the rest of the document: eight of the 15 functions (diagram, voice, collaborative editing, version control, annotations, templates, generative AI or LLM interfaces, previews) never reappear in a use case or requirement, and rich text and translation appear only in requirements.

## What the draft does not cover

Checked against the published draft on 13 November 2026:

- No introduction text and no glossary, though the published draft ends with an empty `glossary` section carrying no heading or content. The working document has a glossary tab ([9 October 2026](https://w3c-cg.github.io/atag/minutes/minutes_Oct09_2026)).
- No AI or agent use case. "AI" and "LLM" each appear once, in the function list; nothing covers agentic or iterative authoring, cost and token warnings, or responsibility chains ([9 October 2026](https://w3c-cg.github.io/atag/minutes/minutes_Oct09_2026), [16 October 2026](https://w3c-cg.github.io/atag/minutes/minutes_Oct16_2026)). Candidate scenarios and the requirements they imply are in [Agentic use cases](../../cg-contributions/contribution-ideas/agentic-use-cases.md).
- No reference to WCAG, EN 301 549, or Section 508, and no conformance discussion.
- Personal-use content is in scope by consensus but not written in ([9 October 2026](https://w3c-cg.github.io/atag/minutes/minutes_Oct09_2026)).
- CAD still carries a TODO asking whether CAD files have accessibility features.
- List items have no stable IDs, the validation section still says "validation" rather than evaluation, and the export use case says "multiple accessible formats" rather than the agreed "one or more" ([16 October 2026](https://w3c-cg.github.io/atag/minutes/minutes_Oct16_2026)).

The draft is edited in a Google Doc and published to ReSpec by the chair between meetings, so it changes in batches rather than through pull requests. Structural decisions behind it are in [Decisions and open questions](../../cg-contributions/open-questions.md); candidate contributions are in [contribution ideas](../../cg-contributions/contribution-ideas/README.md).
