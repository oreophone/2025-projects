# letters-and-numbers
Solvers for the Letters & Numbers game show, implementing fast algorithms that run under the `30s` time limit.

### Letters 
**Specs:**
* Letters _ls_: `str`
* Wordlist _ws_: `List[str]`

**Subtasks:**
* [x] len(_ls_) <= 5, len(_ws_) <= 100
* [x] len(_ls_) == 9, len(_ws_) ~= 50,000 ⭐
- 0.044s [0.042s preprocessing, 0.002s search]
* [x] len(_ls_) <= 30, len(_ws_) ~= 50,000 ⭐⭐
* [x] len(_ls_) <= 256, len(_ws_) <= 500,000 ⭐⭐⭐
- 12.085s [10.78s preprocessing, 1.31s search]

### Numbers
**Specs:**
* Numbers _ns_: `List[int]`
* Target _t_: `int`
* Operations _ops_: `{+,-,*,÷}`

**Subtasks:**
* [ ] len(_ns_) <= 5, ops = `{+,-}`
* [ ] len(_ns_) <= 6
* [ ] len(_ns_) <= 6, solution not guaranteed (return closest to _t_) ⭐
* [ ] len(_ns_) <= 20 ⭐⭐
* [ ] len(_ns_) <= 100 ⭐⭐⭐
