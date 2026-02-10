# Tramrunner

## Installation instructions

```
git clone <repo link>
cd Tramrunner
```
create your virutal envirument and activate it
```
python -m venv .venv
source .venv/bin/activate
```
install dependencies
```
pip install -r requirements.txt
```

## Contents

- `tramrunner/dvb_curses.py`
    - experimente mit curses(ncurses)
- `tramrunner/main.py`
    - useless + broken
- `tramrunner/single_stop_v2.py`
    - built using the dvbpy module https://github.com/offenesdresden/dvbpy
- `tramrunner/static_vvo.py`
    - i don't even know anymore
- `tramrunner/stopinfo_tui.py`
    - working, kinda. using the stuff found in `/api`
- `tramrunner/tramrunner_textual.py`
    - currently working on this
- `tramrunner/trip_info_tui.py`
    - lots of `print`




## using the thing

```
python trammruner/main.py
```