# ATAG 2.0 review findings

From May to July 2026 the group reviewed [ATAG 2.0](https://www.w3.org/TR/ATAG20/) guideline by guideline, looking for "opportunities or gaps" before drafting (Wendy Reid, [31 July 2026](https://w3c-cg.github.io/atag/minutes/minutes_Jul31_2026)). Part A, the authoring tool user interface, was finished on 19 June. Part B, accessible content, ran from 17 July to 31 July.

Part A findings are in the [group wiki](https://github.com/w3c-cg/atag/wiki/Review-of-ATAG-2.0-for-areas-needing-extension-revision); Part B findings exist only in the [minutes](https://w3c-cg.github.io/atag/). No specification edits have been made.

## Editorial updates

| Update                                                                                      | Status   | Source                                                                                                                                    |
| ------------------------------------------------------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| References from WCAG 2.0 to WCAG 2.2, coordinated with AGWG                                 | Agreed   | [27 March 2026](https://www.w3.org/2026/03/27-atag-minutes.html), [22 May 2026](https://w3c-cg.github.io/atag/minutes/minutes_May22_2026) |
| Glossary entries for authoring tool and user agent, covering LLM browsers                   | Proposed | [27 March 2026](https://www.w3.org/2026/03/27-atag-minutes.html)                                                                          |
| Removal of obsolete technologies such as Flash and BlackBerry (W3C change classes 1 and 2)  | Proposed | [27 March 2026](https://www.w3.org/2026/03/27-atag-minutes.html)                                                                          |
| "Developer control" note rephrased to cover third-party plugins                             | Proposed | [22 May 2026](https://w3c-cg.github.io/atag/minutes/minutes_May22_2026)                                                                   |
| Accessibility note for documentation made normative, documentation kept in sync with the UI | Proposed | [19 June 2026](https://w3c-cg.github.io/atag/minutes/minutes_Jun19_2026)                                                                  |

## Proposed additions

| Topic                       | Proposal                                                                                                                                                              | Status                                                                                                                                                         |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AI interfaces               | New guideline A.1.3 for conversational and generative AI functionality, including AI output that becomes part of the interface (Miriam Fukushima, drafted with Saif). | Contested: Ned Zimmerman preferred chat-interface examples in the techniques ([22 May 2026](https://w3c-cg.github.io/atag/minutes/minutes_May22_2026)).        |
| Structure                   | Merge A.1 and A.2, since tools conflate the authoring interface and the editing view; make the generation process perceivable.                                        | Proposed in the wiki.                                                                                                                                          |
| Time and sessions           | Broaden A.3.2 from "enough time" to AI sessions, memory, context loss, waiting and partial output, and step-at-a-time or interruptible agents.                        | Proposed ([5 June 2026](https://w3c-cg.github.io/atag/minutes/minutes_Jun05_2026)).                                                                            |
| Workflow transparency       | Warn before irreversible or costly steps, including token use and usage thresholds.                                                                                   | Proposed ([5 June 2026](https://w3c-cg.github.io/atag/minutes/minutes_Jun05_2026)); in the wiki as "communication of cost or change".                          |
| Version control and history | Undo and redo, dated versions with author names, and separating single-author from collaborative work.                                                                | Proposed ([5 June 2026](https://w3c-cg.github.io/atag/minutes/minutes_Jun05_2026)).                                                                            |
| Collaborative authoring     | Real-time authoring and comment content by other authors.                                                                                                             | Gap identified ([19 June 2026](https://w3c-cg.github.io/atag/minutes/minutes_Jun19_2026)).                                                                     |
| Discrete, editable changes  | Generated output stays editable, and generative tools change content one item at a time so undo stays meaningful.                                                     | Proposed ([19 June 2026](https://w3c-cg.github.io/atag/minutes/minutes_Jun19_2026), [17 July 2026](https://w3c-cg.github.io/atag/minutes/minutes_Jul17_2026)). |
| Deterministic verification  | Tools must prove accessibility claims deterministically, which non-deterministic output cannot.                                                                       | Proposed ([17 July 2026](https://w3c-cg.github.io/atag/minutes/minutes_Jul17_2026)).                                                                           |
| Other gaps                  | Operating system dark, high contrast, and reduced motion preferences; offline and synchronization behavior.                                                           | Gaps and proposals ([19 June 2026](https://w3c-cg.github.io/atag/minutes/minutes_Jun19_2026)).                                                                 |

## Definitions

Terms the review found out of date: **content** (finished versus in progress, computer- versus human-generated), **author**, **authoring tool**, **authoring session**, **automatic**, **generate**, **prompting**, **developer control**, **preferences** and **requirements**, and **display** or **render** rather than present. The group kept a "things to define" list for these ([21 August 2026](https://w3c-cg.github.io/atag/minutes/minutes_Aug21_2026)). The replacement for "prompting" remains open ([4 September 2026](https://w3c-cg.github.io/atag/minutes/minutes_Sep04_2026)), as does defining roles versus actions ([14 August 2026](https://w3c-cg.github.io/atag/minutes/minutes_Aug14_2026)).

## What the review left open

- Whether AI-specific requirements are normative or belong in techniques and best practice (Miriam Fukushima, [31 July 2026](https://w3c-cg.github.io/atag/minutes/minutes_Jul31_2026)).
- Whether AI gets its own part, its own guidelines, or AI-agnostic wording with targeted AI-specific items. This carried into the [Use Cases and Requirements draft](ucr.md).
- How far ATAG should defer to WCAG rather than restate it. Miriam Fukushima proposed treating A.1 as the baseline and writing A.2 onward as deltas ([22 May 2026](https://w3c-cg.github.io/atag/minutes/minutes_May22_2026)).
- Whether the UAAG reference stays ([19 June 2026](https://w3c-cg.github.io/atag/minutes/minutes_Jun19_2026)).

The full register is in [Decisions and open questions](../../cg-contributions/open-questions.md).
