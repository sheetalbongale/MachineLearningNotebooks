# Author: Jake Vanderplas -- <vanderplas@astro.washington.edu>

from collections import OrderedDict
from functools import partial
from time import time

import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import NullFormatter

from sklearn import manifold, datasets

from azureml.core import VERSION as amlversion
from azureml.core import Run
from gensim import __version__ as gsversion
from sklearn import __version__ as skversion
from scipy import __version__ as spversion
from pandas import __version__ as pdversion
from numpy import __version__ as npversion

print(f"Azure ML version: {amlversion}")
print(f"gensim version: {gsversion}")
print(f"sklearn version: {skversion}")
print(f"scipy version: {spversion}")
print(f"numpy version: {npversion}")
print(f"pandas version: {pdversion}")


# Next line to silence pyflakes. This import is needed.
Axes3D

n_points = 1000
X, color = datasets.make_s_curve(n_points, random_state=0)
n_neighbors = 10
n_components = 2

# Create figure
fig = plt.figure(figsize=(15, 8))
fig.suptitle("Manifold Learning with %i points, %i neighbors"
             % (1000, n_neighbors), fontsize=14)

# Add 3d scatter plot
ax = fig.add_subplot(251, projection='3d')
ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=color, cmap=plt.cm.Spectral)
ax.view_init(4, -72)

# Set-up manifold methods
LLE = partial(manifold.LocallyLinearEmbedding,
              n_neighbors, n_components, eigen_solver='auto')

methods = OrderedDict()
# methods['LLE'] = LLE(method='standard')
# methods['LTSA'] = LLE(method='ltsa')
# methods['Hessian LLE'] = LLE(method='hessian')
# methods['Modified LLE'] = LLE(method='modified')
# methods['Isomap'] = manifold.Isomap(n_neighbors, n_components)
# methods['MDS'] = manifold.MDS(n_components, max_iter=100, n_init=1)
# methods['SE'] = manifold.SpectralEmbedding(n_components=n_components,
#                                            n_neighbors=n_neighbors)
methods['t-SNE'] = manifold.TSNE(n_components=n_components, init='pca',
                                 random_state=0)

Y = methods['t-SNE'].fit_transform(X)

df_subset = pd.DataFrame()

df_subset['tsne-2d-one'] = tsne_results[:,0]
df_subset['tsne-2d-two'] = tsne_results[:,1]

print(df_subset.head())

run = Run.get_context()

# Plot results
for i, (label, method) in enumerate(methods.items()):
    t0 = time()
    Y = method.fit_transform(X)
    t1 = time()
    run.log(label, "%.2g sec" % (t1 - t0))
    ax = fig.add_subplot(2, 5, 2 + i + (i > 3))
    ax.scatter(Y[:, 0], Y[:, 1], c=color, cmap=plt.cm.Spectral)
    ax.set_title("%s (%.2g sec)" % (label, t1 - t0))
    ax.xaxis.set_major_formatter(NullFormatter())
    ax.yaxis.set_major_formatter(NullFormatter())
    ax.axis('tight')



run.log_image(name="results", plot=plt)