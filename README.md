## Board Game Geek Popular Mechanics

Extracts mechanics found in games listed in a geeklist and prints the topn (or all) mechanics found in count order.

### Options

|Name |Flag |Description |
|---|---|---|
|Show Counts|--show-counts|Default, displays the number of times a mechanic is found in a geeklist|
|Hide Counts|--hide-counts|hide the count from output|

### Arguments

|Name |Argument |Description |
|---|---|---|
|Geeklist|--geeklist|Geeklist to find mechanics in, can be used multiple times|
|API|--api|Defaults to the How Many Meeple API but can be overwritten for using locally|
|Limit Number of Mechanics|--topn|Specify to limit the number of mechanics returned|

### Example

```bash
python run.py --geeklist 260220 --geeklist 260233 --geeklist 260236 --topn 10 --api localhost:5000 --hide-counts
```

**Returns:**

```
Hand Management
Variable Player Powers
Set Collection
Dice Rolling
Card Drafting
Team-Based Game
Cooperative Game
Tile Placement
Simultaneous Action Selection
Grid Movement
```

