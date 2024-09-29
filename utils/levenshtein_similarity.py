from .levenshtein_distance import levenshtein_distance

def levenshtein_similarity(str1, str2):
    distance = levenshtein_distance(str1, str2)
    max_len = max(len(str1), len(str2))
    return (1 - distance / max_len) * 100