"""STEM-based transportation recommendation tool.

This script scores travel options by combining measurable factors:
- travel time
- total cost
- estimated CO2 emissions

The user can choose how important each factor is (weighting), then the
program calculates a weighted score and recommends the best option.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class TravelOption:
    name: str
    average_speed_mph: float
    cost_per_mile_usd: float
    co2_grams_per_mile: float


TRANSPORT_OPTIONS = [
    TravelOption("Car", average_speed_mph=45, cost_per_mile_usd=0.58, co2_grams_per_mile=400),
    TravelOption("Bus", average_speed_mph=30, cost_per_mile_usd=0.22, co2_grams_per_mile=150),
    TravelOption("Train", average_speed_mph=55, cost_per_mile_usd=0.30, co2_grams_per_mile=90),
    TravelOption("Bike", average_speed_mph=12, cost_per_mile_usd=0.03, co2_grams_per_mile=0),
    TravelOption("Walk", average_speed_mph=3, cost_per_mile_usd=0.00, co2_grams_per_mile=0),
]


def normalize(values: List[float]) -> List[float]:
    """Normalize values to a 0..1 scale where lower values are better.

    If all values are equal, return 0.0 for each entry.
    """
    minimum = min(values)
    maximum = max(values)
    if maximum == minimum:
        return [0.0] * len(values)
    return [(value - minimum) / (maximum - minimum) for value in values]


def recommend_transport(
    distance_miles: float,
    weight_time: float,
    weight_cost: float,
    weight_emissions: float,
):
    times = [distance_miles / option.average_speed_mph for option in TRANSPORT_OPTIONS]
    costs = [distance_miles * option.cost_per_mile_usd for option in TRANSPORT_OPTIONS]
    emissions = [distance_miles * option.co2_grams_per_mile for option in TRANSPORT_OPTIONS]

    norm_times = normalize(times)
    norm_costs = normalize(costs)
    norm_emissions = normalize(emissions)

    scores = []
    for idx, option in enumerate(TRANSPORT_OPTIONS):
        score = (
            weight_time * norm_times[idx]
            + weight_cost * norm_costs[idx]
            + weight_emissions * norm_emissions[idx]
        )
        scores.append((score, option, times[idx], costs[idx], emissions[idx]))

    scores.sort(key=lambda row: row[0])  # Lower is better
    return scores


def get_float(prompt: str, min_value: float = 0.0) -> float:
    while True:
        try:
            value = float(input(prompt).strip())
            if value < min_value:
                print(f"Please enter a value >= {min_value}.")
                continue
            return value
        except ValueError:
            print("Invalid number. Try again.")


def main():
    print("\nTransportation STEM Recommender")
    print("-" * 35)

    distance = get_float("Enter trip distance in miles: ", min_value=0.1)

    print("\nSet importance weights (0 to 1). Higher means more important.")
    weight_time = get_float("Time importance: ", min_value=0.0)
    weight_cost = get_float("Cost importance: ", min_value=0.0)
    weight_emissions = get_float("Emissions importance: ", min_value=0.0)

    total = weight_time + weight_cost + weight_emissions
    if total == 0:
        print("All weights are zero, defaulting to equal weights.")
        weight_time = weight_cost = weight_emissions = 1 / 3
    else:
        weight_time /= total
        weight_cost /= total
        weight_emissions /= total

    ranked = recommend_transport(distance, weight_time, weight_cost, weight_emissions)

    best = ranked[0]
    print("\nBest option:")
    print(
        f"{best[1].name} | Time: {best[2]:.2f} hrs | Cost: ${best[3]:.2f} | "
        f"CO2: {best[4]:.0f} g"
    )

    print("\nFull ranking:")
    for position, (score, option, time_hrs, cost_usd, co2_g) in enumerate(ranked, start=1):
        print(
            f"{position}. {option.name:<6} score={score:.3f} | "
            f"time={time_hrs:.2f} hrs | cost=${cost_usd:.2f} | CO2={co2_g:.0f} g"
        )


if __name__ == "__main__":
    main()
