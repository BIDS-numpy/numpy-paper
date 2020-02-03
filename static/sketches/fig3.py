DejaVu Sans Mono
Size: 62

# Fig. 3

In [1]: import numpy as np

In [2]: import dask.array as da

In [3]: x = da.arange(12)

In [4]: x = np.reshape(x, (4, 3))

In [5]: x
Out[5]: dask.array<..., shape=(4, 3), ...>

In [6]: np.mean(x, axis=0)
Out[6]: dask.array<..., shape=(3,), ...>

In [7]: x = x - np.mean(x, axis=0)

In [8]: x = x / np.std(x, axis=0)

In [9]: x
Out[9]: dask.array<..., shape=(4, 3), ...>


---------

In [1]: import numpy as np

In [2]: import dask.array as da

In [3]: x = da.arange(12)

In [4]: x = np.reshape(x, (4, 3))

In [5]: x
Out[5]: dask.array<reshape, shape=(4, 3), dtype=int64, chunksize=(4, 3), chunktype=numpy.ndarray>

In [6]: np.mean(x, axis=0)
Out[6]: dask.array<mean_agg-aggregate, shape=(3,), dtype=float64, chunksize=(3,), chunktype=numpy.ndarray>

In [7]: x = x - np.mean(x, axis=0)

In [8]: x = x / np.std(x, axis=0)

In [9]: x
Out[9]: dask.array<truediv, shape=(4, 3), dtype=float64, chunksize=(4, 3), chunktype=numpy.ndarray>
