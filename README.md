# colorizer
Easily set outliner and wireframe color in Autodesk Maya.

![Alt text](preview.png?raw=true "Title")

# api

Set outliner color for selection:

```python
import colorizer
colorizer.set_outliner_color('red')
colorizer.set_outliner_color(1.0, 0.0, 0.0)
```

Set wireframe color for selection:

```python
colorizer.set_wireframe_color('green')
colorizer.set_wireframe_color(0.0, 1.0, 0.0)
```

Set both wireframe and outliner color:

```python
colorizer.set_color('blue')
colorizer.set_color(0.0, 0.0, 1.0)
```

Show the Colorizer dialog:

```python
colorizer.ui.show()
```

Available named colors, chosen to be cohesive with the default Maya color theme:

- red
- peach 
- yellow
- green 
- teal
- blue
- purple
- pink
- white 
- black
