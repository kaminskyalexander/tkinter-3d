def intersection(a, b, c, d, x1, y1, z1, x2, y2, z2):

	# Solve for T by using "Ax + By + Cz + D = 0" and subbing in the 
	# parametric linear equation given by the x y and z parameters.
	t = (
		(a*x1 + b*y1 + c*z1 + d) /
		(a*x2 - a*x1 + b*y2 - b*y1 + c*z2 - c*z1)
	)

	# Now that we know t, we can find the point of intersection.
	x = x1 - (x2 - x1) * t
	y = y1 - (y2 - y1) * t
	z = z1 - (z2 - z1) * t

	return x, y, z

