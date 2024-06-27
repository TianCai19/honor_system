import random
from tqdm import tqdm
import time



with tqdm(total=100) as pbar:
    # random time consuming loop
    
    jump_time = random.randint(1, 10)
    sum=0
    while sum<100:
        pbar.update(jump_time)
        time.sleep(0.5)
        jump_time = random.randint(1, 10)
        sum+=jump_time
        print(jump_time)
        