def interpolate(x, lowest, highest, min_value=0, max_value=1):
    return min_value + (max_value - min_value) * (x - lowest) / (highest - lowest)
