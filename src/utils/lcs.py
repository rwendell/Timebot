# Python code for the above approach
from functools import lru_cache
from operator import itemgetter

def longest_common_substring(x: str, y: str):
	
	# function to find the longest common substring

	# Memorizing with maximum size of the memory as 1
	@lru_cache(maxsize=1)
	
	# function to find the longest common prefix
	def longest_common_prefix(i: int, j: int) -> int:
	
		if 0 <= i < len(x) and 0 <= j < len(y) and x[i] == y[j]:
			return 1 + longest_common_prefix(i + 1, j + 1)
		else:
			return 0

	# digonally computing the subproplems
	# to decrease memory dependency
	def digonal_computation():
		
		# upper right trianle of the 2D array
		for k in range(len(x)):	
			yield from ((longest_common_prefix(i, j), i, j)
						for i, j in zip(range(k, -1, -1),
									range(len(y) - 1, -1, -1)))
		
		# lower left triangle of the 2D array
		for k in range(len(y)):	
			yield from ((longest_common_prefix(i, j), i, j)
						for i, j in zip(range(k, -1, -1),
									range(len(x) - 1, -1, -1)))

	# returning the maximum of all the subproblems
	return max(digonal_computation(), key=itemgetter(0), default=(0, 0, 0))

# Driver Code
if __name__ == '__main__':
	x: str = 'GeeksforGeeks'
	y: str = 'GeeksQuiz'
	length, i, j = longest_common_substring(x, y)
	print(f'length: {length}, i: {i}, j: {j}')
	print(f'x substring: {x[i: i + length]}')
	print(f'y substring: {y[j: j + length]}')
