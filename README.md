# Radar

Radar commander is a Python tool for accessing the HLK Radar sensor module via the serial interface.

For internal commands overview and syntax print `help`.  

# Examples

Area detection example.

Proper radar initialization:
```bash
adapter reset
adapter format set 2
```

Set and visualization the areas: 
```bash
adapter area define 1 0 -5 20 -5 10 5 10 5 20
adapter area define 2 0 -5 10 -5 0 5 0 5 10
adapter area define 3 0 -20 30 -20 20 20 20 20 30
adapter area read
```


# Links

Shenzhen Hailingke Electronics Co., Ltd.

https://www.hlktech.net/index.php?id=1185


Radar IC

https://www.iclegend.com/en/product/list/S5KM312CL/