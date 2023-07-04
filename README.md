# MeriCD track converter

Convert MeriCD track from GPX-format to older Nemea-format

## Install
```shell
pipenv install
pipenv shell

convert the script to .exe:  auto-py-to-exe 
```

## Example
```
python3 converter.py --input input/example.GPX --output output/retki.GPS
```

## Run tests
```
python3 -m doctest converter.py
```
