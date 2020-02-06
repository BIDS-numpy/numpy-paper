import numpy as np
x = np.arange(12)
x = x.reshape(4, 3)
x
np.mean(x, axis=0)
x = x - np.mean(x, axis=0)
x

# In [1]: import numpy as np

# In [2]: x = np.arange(12)

# In [3]: x = x.reshape(4, 3)

# In [4]: x
# Out[4]:
# array([[ 0,  1,  2],
#        [ 3,  4,  5],
#        [ 6,  7,  8],
#        [ 9, 10, 11]])

# In [5]: np.mean(x, axis=0)
# Out[5]: array([4.5, 5.5, 6.5])

# In [6]: x = x - np.mean(x, axis=0)

# In [7]: x
# Out[7]:
# array([[-4.5, -4.5, -4.5],
#        [-1.5, -1.5, -1.5],
#        [ 1.5,  1.5,  1.5],
#        [ 4.5,  4.5,  4.5]])
