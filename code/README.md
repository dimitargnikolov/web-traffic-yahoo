# Homogeneity Bias

## Relevant Data
* `$BD/benzene/clicks/sample`
* `$BD/benzene/clicks/fixed-period`

## Outputs
* `$BR/hbias`

## Data Path

1. Compute homogeneity bias.
  `$BC/hbias/compute_hbias.py`

2. Create bar plots.
  `$BC/hbias/plot_hbias.py`

# Popularity Bias

## Relevant Data
* `$BD/benzene/pageranks` contains a list of `domain:pagerank` pairs
* `$BD/benzene/clicks/sample` contains various samples of clicks

## Data Path

1. Compute a list of values for the 100 percentiles of the PageRank data.
  `$BC/pbias/compute_percentile_rank_ranges.py`

2. Compute the popularity bias for the samples of clicks.
  `$BC/pbias/compute_pbias.py`

3. Create QQ plots.
  ``

4. Create bar plots.
  `$BC/pbias/plot_pbias.py`
