# WCAG 3 provisions review

The group is reviewing every provision of the [WCAG 3](https://www.w3.org/TR/wcag-3.0/) draft to decide its relationship to ATAG. The starting point is a spreadsheet of WCAG 3 provisions with a choose-one "Relationship to ATAG" column: **Provision**, **Method**, **Supplemental**, **Informative**, or **None**, plus a free-text notes field (Wendy Reid, [13 November 2026](https://w3c-cg.github.io/atag/minutes/minutes_Nov13_2026)). The provisions under review are listed in [WCAG 3 provisions relevance](wcag-3-provisions-relevance.md).

## Initial choices

For the “Relationship to ATAG” column, the options are:

- **Provision**: Could this be a provision in ATAG, or is there an ATAG provision that could be created from this? (Provision = success criteria)
- **Method**: Would ATAG offer a method for this provision?
- **Supplemental**: Would ATAG offer a supplemental resource for this provision?
- **Informative**: Is this provision related to ATAG, but in an informative way (not a requirement, but referring to this provision would help make a provision in ATAG clearer)?
- **None**: There is no relationship between ATAG and WCAG for this provision outside of the established one (ATAG-compliant authoring tools conform to WCAG)

## Proposed choices

The discussion in [ATAG#38] proposes replacing those choices, and allowing more than one per provision:

| Proposed choice                                 | Relationship it records                                                                                                                                |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Add a core provision in ATAG for this provision | ATAG gains an equivalent requirement. Participants doubted this applies to any provision.                                                              |
| Add a supplemental provision in ATAG            | ATAG gains a requirement that supports, but does not duplicate, the WCAG provision. Participants doubted this applies to any provision.                |
| Add a method in WCAG                            | WCAG gains a method describing how an authoring tool helps authors meet the provision, by enabling, prompting for, or checking the accessible outcome. |
| Add informative content in WCAG                 | WCAG refers readers to ATAG without adding requirements.                                                                                               |
| High, medium, or low ATAG relevance             | Replaces the binary "None" answer with a graded one. Participants expected no provision to be truly unrelated.                                         |
| Unclear                                         | The group has open questions before it can classify the provision.                                                                                     |

## Open questions

The exercise covers the ATAG relationship to content requirements only, equivalent to ATAG 2.0 Part B; every WCAG provision is assumed to apply to the authoring tool's own interface, as in Part A. Open questions from the 13 November meeting:

- **Two ways of testing.** Members argued every provision is potentially related to ATAG, so classification should record which relationship applies rather than whether one exists (Mitchell Evan).
- **Per tool type.** Relevance varies by category of authoring tool, so a single classification may need a tool-type dimension (Miriam Fukushima). The chair preferred keeping the first pass high level.
- **Methods are unsettled.** AGWG has not published a format for WCAG 3 methods. One method may satisfy several provisions, and meeting a provision may need both the authoring tool capability and the author's action (Lisa Liskovoi, Mitchell Evan).
- **Conformance testing is out of scope for now.** Identifying ATAG as a WCAG method should not widen WCAG testing, but could open the door to an ATAG conformance evaluation (Charles Hall, Miriam Fukushima).

The group also wants ATAG to be named in WCAG 3 where relevant, because vendors and authors look to WCAG rather than ATAG, and authoring tools shape conformance from the start. See [ATAG CG](../../knowledge-base/atag-cg/README.md#status) for where this fits among CG work items.
