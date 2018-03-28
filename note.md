
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