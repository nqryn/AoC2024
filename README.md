# AoC2024


### Creation template

```
for i in {1..25}; do
  mkdir "d$i"                          # Create the directory
  cp sol.py "d$i/sol.py"               # Copy sol.py into the directory
  touch "d$i/f.in" "d$i/f_test.in"     # Create empty files f.in and f_test.in
done
```