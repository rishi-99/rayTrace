# RayTrace

## About

A simple environment for bots which can sense its surrounding using ray traces as sensor element. Rays emiting at each 
degree of rotation acts as sensor which senses the distance of obstacle from its current position. Hence N degree of view
angle will return a dictionary of degree value and its respective obstacle distance sensed. This information is processed 
in developed models for making decession of direction and move. This environment cam be created by adding objects (walls)
can be customized as per user requierements. 




[![Bots Interaction](https://github.com/rishi-99/rayTrace/blob/master/ezgif.com-optimize.gif)


[![Bots sensing walls](https://github.com/rishi-99/rayTrace/blob/master/training.gif)


[![Bots in open field](https://github.com/rishi-99/rayTrace/blob/master/hidenseek.gif)




# Requirements 
All below modules in python 3.6 and above

- opencv-python 

```python

pip install opencv-python
```
- Numpy
```python

pip install numpy
```

## Execution 

Run 'randomWalk.py' or 'controlledWalk.py' with python3.







