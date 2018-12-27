from saxpy.alphabet import cuts_for_asize
# # cuts_for_asize(3)
#
# import numpy as np
# from saxpy.znorm import znorm
# from saxpy.sax import ts_to_string
# test = ts_to_string(znorm(np.array([-2, 0, 2, 0, -1] * 2)), cuts_for_asize(20))
#
# print(test)

import numpy as np
from saxpy.znorm import znorm
from saxpy.paa import paa
from saxpy.sax import ts_to_string

dat = np.array([-2, 0, 2, 0, -1] * 2)
dat_znorm = znorm(dat)
dat_paa_5 = paa(dat_znorm, 5)

print(ts_to_string(dat_paa_5, cuts_for_asize(3)))