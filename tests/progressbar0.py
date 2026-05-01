import time
import numpy as np
from progress.bar import IncrementalBar

mylist = np.linspace(0, 10, 100)

bar = IncrementalBar('Countdown', max = len(mylist))

for item in mylist:
    bar.next()
    time.sleep(0.1)

bar.finish()
