# import numpy as np
# import matplotlib.pyplot as plt
#
# # Parameters
# n_samples, n_features = 100, 48
#
# # Toy dataset
# rng = np.random.RandomState(41)
# X = rng.randn(n_samples, n_features)
#
# # Plot the first time series
# plt.plot(X[0])
# plt.show()

import sys

# print(sys.executable)

import vamp
import librosa

# import future
import numpy as np
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
from scipy.stats import norm
from pyts.quantization import SAX

# Parameters
# n_samples, n_features = 100, 12
# n_samples, n_features = 100, 12


# Toy dataset
# rng = np.random.RandomState(41)
# X = rng.randn(n_samples, n_features)
# x = y = z = np.arange(0.0,5.0,1.0)
# np.savetxt('test.out', x, delimiter=',')   # X is an array
# >>> np.savetxt('test.out', (x,y,z))   # x,y,z equal sized 1D arrays
# >>> np.savetxt('test.out', x, fmt='%1.4e')   # use exponential notation

# Parameters
# n_samples, n_features = 100, 12
#
# # Toy dataset
# rng = np.random.RandomState(41)
# X = rng.randn(n_samples, n_features)
#
# exit(0)
# SAX transformation
n_bins = 26  # 3
quantiles = 'empirical'
sax = SAX(n_bins=n_bins, quantiles=quantiles)

data, rate = librosa.load("/Users/elliottevers/Documents/DocumentsSymlinked/git-repos.nosync/audio/youtube/tswift_teardrops.wav")

# TODO: melody extraction
melody = vamp.collect(data, rate, "mtg-melodia:melodia")

# type(melody['vector'][1])

n_samples, n_features = melody['vector'][1].shape, 1

# X = melody['vector'][1].reshape(melody['vector'][1].shape[0], 1)
X = melody['vector'][1].reshape(1, melody['vector'][1].shape[0])

X[X <= 0] = 0

# X_sax = sax.fit_transform(X).reshape(-1,)
X_sax = sax.fit_transform(X)

# Compute gaussian bins
bins = norm.ppf(np.linspace(0, 1, n_bins + 1)[1:-1])

# flattened = X_sax.flatten()

np.savetxt('test.txt', X_sax.reshape(X_sax.shape[1],),  delimiter=',', fmt='%s')

# # Show the results for the first time series
# plt.figure(figsize=(12, 8))
# plt.plot(X[0], 'o-', label='Original')
# for x, y, s in zip(range(X[0].shape[0]), X[0], X_sax[0]):
#     plt.text(x, y, s, ha='center', va='bottom', fontsize=24, color='#ff7f0e')
# plt.hlines(bins, 0, n_features, color='g', linestyles='--', linewidth=0.5)
# sax_legend = mlines.Line2D([], [], color='#ff7f0e', marker='*',
#                            label='SAX - {0} bins'.format(n_bins))
# first_legend = plt.legend(handles=[sax_legend], fontsize=14, loc=4)
# ax = plt.gca().add_artist(first_legend)
# plt.legend(loc='best', fontsize=14)
# plt.show()