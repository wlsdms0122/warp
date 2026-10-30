# Examples

Programs written in Warp, each one or more documents. A program holds its state, its rules and what it prints; a host builds it and runs it from an entry, and lends it the vocabulary it calls beyond the standard one. Any host that lends the same vocabulary runs the same documents.

| folder | documents | entry | what it is |
|---|---|---|---|
| `snake/` | 1 | `game.main(width, height)` | the game in a terminal: the board drawn as text, arrows or `wasd` to turn, `q` to quit |
| `todo/` | 1 | `todo.main(command, text?, number?)` | a list kept in `todo.json`: `add`, `done`, `list` |
| `wordfreq/` | 1 | `words.main(path, top?)` | the most frequent words of a text file |
| `fetch/` | 1 | `fetch.main(url)` | GET a url and describe the response; a failed request is caught |
| `orders/` | 2 | `orders.main(path, server)` | order lines read from JSON, bad ones skipped with the reason, totalled through `money`, a summary POSTed and a receipt written |
| `flow/` | 13 | `flow.main(path, report?)` | a workflow runner: a plan in `plan/` names steps, each step kind is a document claiming one contract, and the return value is how many steps failed |
| `sheet/` | 7 | `sheet.main(path, out?)` | a spreadsheet: formulas parsed by recursive descent, cells computed level by level with each level at once, the grid written as text and JSON; sheets in `input/` |
| `feature/` | 1 to 5 each | per program | 88 programs, each asking the language one thing, listed in `programs.tsv` |

A program's documents are handed to the build together, in any order. A program reads and writes files under the directory it is run in.

## What a host lends

The standard vocabulary is the specification's. The rest is a host's, and these programs call the following:

| name | parameters | returns | fails with | called by |
|---|---|---|---|---|
| `IO.key` | | `String?`, the key pressed, null when none is | | snake |
| `IO.write` | `text: String` | `Null` | | snake, todo, wordfreq, fetch, orders, flow, sheet |
| `IO.clear` | | `Null` | | snake |
| `Time.now` | | `Int`, milliseconds | | flow |
| `Time.wait` | `milliseconds: Int` | `Null` | | snake, flow |
| `Random.int` | `under: Int` | `Int` from 0 below `under`, isolated | | snake |
| `File.read` | `path: String` | `String?`, null when there is no such file | `file_failed` | todo, wordfreq, orders, flow, sheet |
| `File.write` | `path: String`, `text: String` | `Null` | `file_failed` | todo, orders, flow, sheet |
| `File.exists` | `path: String` | `Bool` | `file_failed` | |
| `File.list` | `path: String` | `Array<String>` | `file_failed` | |
| `Net.get` | `url: String`, `headers: Dictionary<String, String>?` | `Net.Response { body: String, headers: Dictionary<String, String>, status: Int }` | `net_failed` | fetch, flow |
| `Net.post` | `url: String`, `body: String`, `headers: Dictionary<String, String>?` | `Net.Response` | `net_failed` | orders |
| `JSON.parse` | `of: String` | `Any`, const and isolated | `json_failed` | todo, fetch, orders, flow, sheet |
| `JSON.text` | `of: Any` | `String`, const and isolated | `json_failed` | todo, orders, flow, sheet |
| `Process.run` | `command: String` | `Process.Result { output: String, status: Int }` | `process_failed` | flow |
| `Host.issue` | | `Host.Ticket { id: Int }` | | feature |
| `Host.redeem` | `of: Host.Ticket` | `Int`; refuses a ticket that is not open | | feature |
| `Host.log` | `of: Any` | `Null` | | feature |
| `Host.put` | `key: String`, `value: Any` | `Null` | | feature |
| `Host.get` | `key: String` | `Any` | | feature |

A path that leads out of the directory the program is run in fails with `file_failed`. `fetch`, `orders` and `flow` talk to a local server, `tool/server.py`, which serves the files under a directory and responds to a POST with `201 {"id": 7}`:

```
python3 tool/server.py 8765 orders
```

## The feature table

`feature/programs.tsv` has one row per program, tab separated:

| column | what |
|---|---|
| `name` | the program |
| `documents` | its documents in `feature/`, without `.warpt` |
| `entry` | the procedure it is run from |
| `arguments` | `name=value` pairs, a value written as the text writes one |
| `laid` | `together`: handed to the build at once; `in order`: each laid against the ones before it, the way a document that arrives later is |
| `expects` | `answers`, or the stage that refuses it: `refuses at the load`, `the build` or `the run` |
| `asks` | what the program asks of the language |
