

''' Coding Challenge

	write a funciton that inputs a square 2d matrix (as a list of lists)
	that outputs a matrix of the same size with the values rotated
	clockwise, except for the values along the diagonal lines (aka an X,
	through the matrix)

	'''

m = [
	[1,  2,  3,  4,   5],
	[6,  7,  8,  9,  10],
	[11, 12, 13, 14, 15],
	[16, 17, 18, 19, 20],
	[21, 22, 23, 24, 25]
]

def r(m):

	s = len(m)

	def diagonal(x, y):
		return x == y or x == s - y - 1

	m2 = []
	for x in range(s):
		row = []
		for y in range(s):
			row.append(m[x][y] if diagonal(x, y) else m[s - y - 1][x])
		m2.append(row)
	return m2

def print2d_arr(arr2d):
	for row in arr2d:
		s = ''
		for x in row:
			if len(str(x)) == 1:
				s += ' '
			s += ' ' + str(x)
		print(s)

print('\nInput:')
print2d_arr(m)
print('\nOutput:')
print2d_arr(r(m))
print()