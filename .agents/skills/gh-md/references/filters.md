# CEL filters

Filter local items with `gh md --list --filter '<expression>'`. See [the skill](../SKILL.md) for context. Filters only see files under the current `GH_MD_ROOT`; pull first.

Expressions use [Common Expression Language](https://cel.dev/). Wrap the whole expression in single quotes and strings inside it in double quotes. An invalid expression fails with a compile error that points at the problem.

## Variables

| Variable    | Type      | Notes                                        |
| ----------- | --------- | -------------------------------------------- |
| `item_type` | string    | `issue`, `pr`, or `discussion`               |
| `state`     | string    | `open` or `closed`; PRs can also be `merged` |
| `title`     | string    |                                              |
| `body`      | string    | Issue, PR, or discussion body                |
| `author`    | string    | GitHub login                                 |
| `assigned`  | list      | Assignee logins                              |
| `reviewers` | list      | Requested reviewer logins                    |
| `labels`    | list      | Label names                                  |
| `created`   | timestamp |                                              |
| `updated`   | timestamp |                                              |
| `owner`     | string    |                                              |
| `repo`      | string    |                                              |
| `number`    | int       |                                              |
| `user`      | string    | Authenticated user's login                   |
| `now`       | timestamp | Current time                                 |

## Recipes

```sh
# State and type
gh md --list --filter 'state == "open"'
gh md --list --filter 'item_type == "pr" && state == "merged"'
gh md --list --filter 'item_type != "discussion" && state != "open"'

# Labels
gh md --list --filter '"bug" in labels'
gh md --list --filter 'labels.exists(l, l.startsWith("priority:"))'
gh md --list --filter 'labels.size() == 0 && state == "open"'     # untriaged

# People
gh md --list --filter 'author == user'
gh md --list --filter 'user in reviewers && state == "open"'       # review requests
gh md --list --filter 'user in assigned && state == "open"'     # same as --assigned

# Dates (durations use h, m, s; no d unit)
gh md --list --filter 'updated > now - duration("168h")'           # last 7 days
gh md --list --filter 'state == "open" && updated < now - duration("2160h")'   # stale for 90 days
gh md --list --filter 'created >= timestamp("2026-01-01T00:00:00Z")'

# Text
gh md --list --filter 'title.lowerAscii().contains("accessibility")'
gh md --list --filter 'body.contains("WCAG")'
gh md --list --filter 'title.matches("(?i)^rfc[: ]")'

# Scope
gh md --list --filter 'owner == "w3c-cg" && repo == "atag" && number >= 100'
```

Combine filters with `&&`, `||`, and `!`, and with the type flags `--issues`, `--prs`, `--discussions`, and `--assigned`. A positional `owner/repo` argument narrows to one repository.

## Scripting

```sh
# Paths of matching files
gh md --list --format=json --filter 'state == "open"' | jq -r '.[].file_path'

# Counts by type and state
gh md --list --format=json | jq -r 'group_by(.type + " " + .state)[] | "\(.[0].type) \(.[0].state): \(length)"'
```

JSON and YAML items have `owner`, `repo`, `number`, `type`, `state`, `title`, `url`, and `file_path`. For dates, labels, or authors in output, read the front matter of each file.
