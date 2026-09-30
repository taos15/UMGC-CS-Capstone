from skillmatch.features.matching.schemas import Recommendation


def rank_recommendations(
    recommendations: list[Recommendation], minimum_score: float, top_k: int
) -> list[Recommendation]:
    return sorted(
        (item for item in recommendations if item.score >= minimum_score),
        key=lambda item: item.score,
        reverse=True,
    )[:top_k]
