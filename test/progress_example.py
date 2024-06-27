from progress.bar import Bar
import time

bar = Bar('Processing', max=300)
for i in range(300):
    time.sleep(0.1)
    bar.next()
bar.finish()