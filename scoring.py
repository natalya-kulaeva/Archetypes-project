Модуль подсчёта баллов для теста архетипов

def calculate_scores(user_answers, questions_data):
    scores = {i: 0 for i in range(1, 13)}
    
    for question_index, answer_index in enumerate(user_answers):
        question = questions_data['questions'][question_index]
        selected_option = question['options'][answer_index]
        
        archetype_id = selected_option['archetype_id']
        points = selected_option['points']
        
        scores[archetype_id] += points
    
    return scores

def get_top_3_archetypes(scores, archetypes_data):
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_3_ids = [item[0] for item in sorted_scores[:3]]
    
    top_3 = []
    for arch_id in top_3_ids:
        arch_data = next(
            (a for a in archetypes_data['archetypes'] if a['id'] == arch_id),
            None
        )
        if arch_data:
            score = scores[arch_id]
            top_3.append((arch_data, score))
    
    return top_3

def get_all_archetypes_with_scores(scores, archetypes_data):
    all_archetypes = []
    
    for archetype in archetypes_data['archetypes']:
        arch_id = archetype['id']
        score = scores[arch_id]
        all_archetypes.append((archetype, score))
    
    return all_archetypes

def scores_to_percentages(scores):
    max_score = max(scores.values()) if scores.values() else 1
    
    if max_score == 0:
        return {arch_id: 0 for arch_id in scores}
    
    percentages = {}
    for arch_id, score in scores.items():
        percentage = round((score / max_score) * 100)
        percentages[arch_id] = percentage
    
    return percentages

def analyze_profile_type(scores):
    max_score = max(scores.values())
    max_count = sum(1 for s in scores.values() if s == max_score)
    
    if max_score >= 9 and max_count == 1:
        return "focused"
    
    if max_count >= 4:
        return "balanced"
    
    return "diverse"
