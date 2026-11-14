# File format

Each item is one Markdown file with YAML front matter and HTML comment markers. See [the skill](../SKILL.md) for the edit and push workflow.

```markdown
---
id: I_kwDOQUFZWc7Y6-gO
url: https://github.com/owner/repo/issues/123
number: 123
owner: owner
repo: repo
title: Example issue
state: open
author: octocat
labels: [bug, help wanted]
assignees: [octocat]
created: 2026-01-01T00:00:00Z
updated: 2026-01-24T12:00:00Z
last_pulled: 2026-01-24T12:30:00Z
---

<!-- gh-md:content -->

# Example issue

Issue body.
<!-- /gh-md:content -->

---

<!-- gh-md:comment
id: IC_kwDOQUFZWc7a6bI9
author: octocat
created: 2026-01-02T00:00:00Z
-->

### @octocat (2026-01-02)

Comment body.
<!-- /gh-md:comment -->

<!-- gh-md:new-comment -->

<!-- /gh-md:new-comment -->
```

## Front matter

Common fields: `id`, `url`, `number`, `owner`, `repo`, `title`, `state`, `author`, `created`, `updated`, and `last_pulled`. Empty lists such as `labels` and `assignees` are omitted.

Type-specific fields:

- Pull requests: `head_ref`, `base_ref`, and, once merged, `merged` and `merge_commit`. `state` can be `merged`.
- Discussions: `category`.

Only `title` and `state` are pushable. Leave the other fields alone: they identify the item and drive conflict detection.

## Body and comments

- The `# Title` heading at the top of the content block is generated from the title. Change the title in front matter instead.
- Comments appear in chronological order. Each `### @login (date)` heading is generated; edit only the text below it.
- Pull request files also include review comments as read-only context.
- Text outside the markers, such as the `---` separator after the body, is not pushed.

## Edit examples

Add a comment:

```markdown
<!-- gh-md:new-comment -->

Thanks, confirmed on the latest release. Closing as fixed.
<!-- /gh-md:new-comment -->
```

Close the issue in the same push by setting `state: closed` in front matter. Then run `gh md push --dry-run <file>` and check the preview before `gh md push <file>`.
