# Epicycloides
Provides an animation of circles drawing the epicycloïde corresponding to a closed line

scripts need to be run in this order :
  - contour.py
  - tri_points.py
  - trace.py

contour.py creates a .txt file which stores the pixels of the contour

tri_points.py sorts all this pixels to be able to determinate 2 parametric equations (one for the x-axis, the other for th y-axis) and creates a new .txt file

trace.py creates the animation from the .txt file created by tri_points.py

There are some examples for different numbers of circles involved in the epicycloïde.
