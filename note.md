
## Data processing

SPX Member Weights: cannot obtain from bloomberg - need pro account..

Daily data: as early as 1986 (maybe earlier than this)

Hi-Freq data/by minutes: within 140 days

### Hyperparameters
RNN interval: use day1-day8 to predict day9



## References
[Understanding LSTM Networks](http://colah.github.io/posts/2015-08-Understanding-LSTMs/)



crawl all historical member securities -> union

crawl all historical data (30 years are enough)

matrix[0]
companies   HIGH    LOW     VOL     OPEN        CLOSE       IN_MEMBER
---         0.000   0.000   0.000   0.000       0.000       1
---
---

---         0.000   0.000   0.000   0.000       0.000       1
---         0.000   0.000   0.000   0.000       0.000       0
---         0.000   0.000   0.000   0.000       0.000       0
---         0.000   0.000   0.000   0.000       0.000       1
---         0.000   0.000   0.000   0.000       0.000       0
...

use matrix[0] ~ matrix[p] to predict matrix[p+1]




## Useful Directories stored on Bloomberg lab PC:
Bloomberg lab - the spot nearest to the door..
Credential

LIANSAIDONG
~AliXXxxxxx+~

Personal documents: \Downloads

Python-3.4.4 directory + codes: C:\Users\ld273\python34\Python-3.4.4

Python path: C:\ProgramData\Anaconda3\python.exe

Anaconda3: C:\Users\ld273\AppData\Local\Continuum\anaconda3





Row/Obs: 365 x Years_train
Col/Features: 500 x 5(OCHL+volume) x num. of intervals (e.g. day1-day9 predict day10)