# F1DriverRating
A rating system for F1 drivers

---

## How it works

Each driver starts off with 1350 rating. In each race, the drivers are sorted by rating and each driver is given a predicted finishing position. Each driver also gets an adjustment based on finishing position. First place gets an adjustment of half the number of drivers in the field. The next position gets one less and so on. Past the halfway mark, the drivers get a negative adjustment. The positions gained by the driver is calculated by taking the prediction, subtracting the actual finish and then adding the adjustment. 

The positives and negatives are each summed. A share of points is calculated based on the driver's positions gained out of the total positions gained. This share percentage is then taken form the total pool of points available and then added to (or subtracted from) a driver's rating. If a driver drops below 100 points, they no longer lose points and are not counted in the total if they will not gain any points from the race.

This is not a completely perfect rating as instances where drivers do not finish are not counted. There's no easy way to know whether a driver failed to finish because of their own error or through a freak mechanical malfunction. I don't think it would be fair to judge a driver's skill based on a loss due to something out of their control. I think a rating that only affected by races the driver actually finishes is the most accurate that I can get this.
