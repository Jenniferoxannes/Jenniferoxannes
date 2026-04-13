## Transportation STEM Program

This repository now includes a small STEM-based transportation recommender:

- File: `transport_optimizer.py`
- Purpose: estimate the **best way to travel** based on measurable factors:
  - travel time
  - travel cost
  - CO2 emissions

### How it works

1. Enter distance in miles.
2. Set importance weights for time, cost, and emissions.
3. The program normalizes each metric and calculates a weighted score.
4. It returns the best option and a full ranking across:
   - Car
   - Bus
   - Train
   - Bike
   - Walk

### Run

```bash
python3 transport_optimizer.py
```

### Example use case

If you care more about low emissions and low cost than speed, increase those weights.
The recommendation will shift toward options like train, bike, or walking for shorter distances.
