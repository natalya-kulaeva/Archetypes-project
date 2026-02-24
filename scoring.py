Модуль подсчёта баллов для теста архетипов

Логика:
Пользователь отвечает на 8 вопросов
Каждый ответ даёт 3 балла одному архетипу
Максимум у одного архетипа: 9 баллов (если выбран 3 раза)
Результат: топ-3 архетипа + все 12 с баллами



def calculate_scores(user_answers, questions_data):
    
    Подсчитывает баллы по всем архетипам
    
    Параметры:
        user_answers: список индексов выбранных вариантов [0, 1, 2, 0, ...]
                     Длина = количество вопросов (8)
        questions_data: данные из questions.json
    
    Возвращает:
        scores: словарь {archetype_id: points}
                Например: {1: 6, 2: 0, 3: 9, ...}
    
    Инициализация баллов (все архетипы с 0 баллов)
    scores = {i: 0 for i in range(1, 13)}
    
    Пройтись по каждому вопросу
    for question_index, answer_index in enumerate(user_answers):
        Получить данные вопроса
        question = questions_data['questions'][question_index]
        
        Получить выбранный вариант ответа
        selected_option = question['options'][answer_index]
        
        Извлечь архетип и баллы
        archetype_id = selected_option['archetype_id']
        points = selected_option['points']
        
        Добавить баллы к архетипу
        scores[archetype_id] += points
    
    return scores


def get_top_3_archetypes(scores, archetypes_data):
    
    Находит топ-3 архетипа с максимальными баллами
    
    Параметры:
        scores: словарь {archetype_id: points}
        archetypes_data: данные из archetypes.json
    
    Возвращает:
        Список кортежей [(archetype_data, score), (archetype_data, score), ...]
        Отсортировано по убыванию баллов
    
    Сортировать архетипы по баллам (от большего к меньшему)
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    Взять топ-3 ID
    top_3_ids = [item[0] for item in sorted_scores[:3]]
    
    Найти данные архетипов из archetypes.json
    top_3 = []
    for arch_id in top_3_ids:
        # Найти архетип по ID
        arch_data = next(
            (a for a in archetypes_data['archetypes'] if a['id'] == arch_id),
            None
        )
        if arch_data:
            score = scores[arch_id]
            top_3.append((arch_data, score))
    
    return top_3


def get_all_archetypes_with_scores(scores, archetypes_data):
    
    Возвращает все 12 архетипов с их баллами
    
    Параметры:
        scores: словарь {archetype_id: points}
        archetypes_data: данные из archetypes.json
    
    Возвращает:
        Список кортежей [(archetype_data, score), ...]
        Отсортировано по ID архетипа (1-12)
    
    all_archetypes = []
    
    for archetype in archetypes_data['archetypes']:
        arch_id = archetype['id']
        score = scores[arch_id]
        all_archetypes.append((archetype, score))
    
    return all_archetypes


def scores_to_percentages(scores):
    
    Конвертирует баллы в проценты для визуализации
    
    Параметры:
        scores: словарь {archetype_id: points}
    
    Возвращает:
        Словарь {archetype_id: percentage}
        Процент рассчитывается относительно максимального балла
    
    Найти максимальный балл
    max_score = max(scores.values()) if scores.values() else 1
    
    Если все баллы = 0, вернуть нули
    if max_score == 0:
        return {arch_id: 0 for arch_id in scores}
    
    Рассчитать проценты
    percentages = {}
    for arch_id, score in scores.items():
        percentage = round((score / max_score) * 100)
        percentages[arch_id] = percentage
    
    return percentages


def get_primary_archetype(scores, archetypes_data):
    
    Определяет ОСНОВНОЙ архетип (с максимальными баллами)
    
    Возвращает:
        Кортеж (archetype_data, score) или (None, None) если все равны
    
    Найти максимальный балл
    max_score = max(scores.values())
    
    Найти все архетипы с максимальным баллом
    primary_ids = [arch_id for arch_id, score in scores.items() if score == max_score]
    
    Если несколько архетипов с одинаковым максимумом
    if len(primary_ids) > 3:
        Сбалансированный профиль
        return (None, max_score)
    
    Взять первого (или случайного)
    primary_id = primary_ids[0]
    
    Найти данные архетипа
    primary_data = next(
        (a for a in archetypes_data['archetypes'] if a['id'] == primary_id),
        None
    )
    
    return (primary_data, max_score)


def analyze_profile_type(scores):
    
    Анализирует тип профиля пользователя
    
    Возвращает:
        Строку с типом: "focused" / "balanced" / "diverse"
    
    max_score = max(scores.values())
    non_zero_scores = [s for s in scores.values() if s > 0]
    
    Подсчитать архетипы с максимальным баллом
    max_count = sum(1 for s in scores.values() if s == max_score)
    
    Явный лидер (один архетип явно доминирует)
    if max_score >= 9 and max_count == 1:
        return "focused"  Сфокусированный профиль
    
    Сбалансированный (несколько архетипов одинаково)
    if max_count >= 4:
        return "balanced" Сбалансированный
    
    Разнообразный (много архетипов, но есть лидеры)
    return "diverse"  Разнообразный


def get_interpretation(profile_type, primary_archetype):
    
    Возвращает текстовую интерпретацию результата
    
    Параметры:
        profile_type: тип профиля ("focused" / "balanced" / "diverse")
        primary_archetype: данные основного архетипа или None
    
    Возвращает:
        Строку с интерпретацией
    
    if profile_type == "focused":
        return f"У вас ЯРКО ВЫРАЖЕННЫЙ архетип: {primary_archetype['name']}. Это ваша главная черта личности."
    
    elif profile_type == "balanced":
        return "У вас СБАЛАНСИРОВАННЫЙ профиль. Вы многогранная личность без явного доминирующего архетипа. Это говорит о гибкости и адаптивности."
    
    else: = "diverse"
        return f"У вас РАЗНООБРАЗНЫЙ профиль с ведущим архетипом {primary_archetype['name'] if primary_archetype else 'неопределённым'}. Вы сочетаете черты нескольких типов личности."


# ТЕСТИРОВАНИЕ 

if __name__ == "__main__":
    print("=" * 60)
    print("ТЕСТИРОВАНИЕ ЛОГИКИ ПОДСЧЁТА БАЛЛОВ")
    print("=" * 60)
    
    Загрузка тестовых данных
    import json
    
    Мок-данные для теста (упрощённые)
    questions_mock = {
        "questions": [
            {
                "id": 1,
                "options": [
                    {"archetype_id": 5, "points": 3},  Искатель
                    {"archetype_id": 6, "points": 3},  Правитель
                    {"archetype_id": 1, "points": 3}   Славный малый
                ]
            },
            {
                "id": 2,
                "options": [
                    {"archetype_id": 12, "points": 3}, Эстет
                    {"archetype_id": 3, "points": 3},  Мудрец
                    {"archetype_id": 4, "points": 3}   Маг
                ]
            },
            {
                "id": 3,
                "options": [
                    {"archetype_id": 7, "points": 3},  Заботливый
                    {"archetype_id": 8, "points": 3},  Бунтарь
                    {"archetype_id": 3, "points": 3}   Мудрец
                ]
            },
            {
                "id": 4,
                "options": [
                    {"archetype_id": 2, "points": 3},  Герой
                    {"archetype_id": 9, "points": 3},  Шут
                    {"archetype_id": 10, "points": 3}  Невинный
                ]
            },
            {
                "id": 5,
                "options": [
                    {"archetype_id": 11, "points": 3}, Творец
                    {"archetype_id": 5, "points": 3},  Искатель
                    {"archetype_id": 10, "points": 3}  Невинный
                ]
            },
            {
                "id": 6,
                "options": [
                    {"archetype_id": 7, "points": 3},  Заботливый
                    {"archetype_id": 6, "points": 3},  Правитель
                    {"archetype_id": 1, "points": 3}   Славный малый
                ]
            },
            {
                "id": 7,
                "options": [
                    {"archetype_id": 12, "points": 3}, Эстет
                    {"archetype_id": 3, "points": 3},  Мудрец
                    {"archetype_id": 11, "points": 3}  Творец
                ]
            },
            {
                "id": 8,
                "options": [
                    {"archetype_id": 6, "points": 3},  Правитель
                    {"archetype_id": 4, "points": 3},  Маг
                    {"archetype_id": 7, "points": 3}   Заботливый
                ]
            }
        ]
    }
    
    archetypes_mock = {
        "archetypes": [
            {"id": i, "name": f"Архетип {i}"} for i in range(1, 13)
        ]
    }
    
    ТЕСТ 1: Пользователь выбрал всегда вариант B (Мудрец 3 раза)
    print("\n--- ТЕСТ 1: Выбраны ответы [0, 1, 2, 0, 1, 0, 1, 2] ---")
    user_answers_1 = [0, 1, 2, 0, 1, 0, 1, 2]
    
    scores_1 = calculate_scores(user_answers_1, questions_mock)
    print("Баллы:", scores_1)
    
    Проверка: Мудрец должен иметь 9 баллов (3 раза по 3)
    assert scores_1[3] == 9, f"Ошибка! Мудрец должен иметь 9, получено {scores_1[3]}"
    print("✅ Мудрец: 9 баллов (правильно!)")
    
    Топ-3
    top_3_1 = get_top_3_archetypes(scores_1, archetypes_mock)
    print("Топ-3:", [(a[0]['name'], a[1]) for a in top_3_1])
    
    Проценты
    percentages_1 = scores_to_percentages(scores_1)
    print("Проценты (топ-5):")
    sorted_perc = sorted(percentages_1.items(), key=lambda x: x[1], reverse=True)[:5]
    for arch_id, perc in sorted_perc:
        print(f"  Архетип {arch_id}: {perc}%")
    
    ТЕСТ 2: Равномерное распределение
    print("\n--- ТЕСТ 2: Все архетипы по разу ---")
    user_answers_2 = [0, 0, 0, 0, 0, 0, 0, 0]  Всегда вариант A
    
    scores_2 = calculate_scores(user_answers_2, questions_mock)
    print("Баллы:", scores_2)
    
    Искатель, Эстет, Заботливый, Герой, Творец, Заботливый (2 раза!), Эстет (2 раза!), Правитель
    Значит: Заботливый = 6, Эстет = 6, остальные по 3
    
    top_3_2 = get_top_3_archetypes(scores_2, archetypes_mock)
    print("Топ-3:", [(a[0]['name'], a[1]) for a in top_3_2])
    
    # ТЕСТ 3: Основной архетип
    print("\n--- ТЕСТ 3: Определение основного архетипа ---")
    primary = get_primary_archetype(scores_1, archetypes_mock)
    if primary[0]:
        print(f"Основной архетип: {primary[0]['name']} ({primary[1]} баллов)")
        assert primary[0]['id'] == 3, "Основной должен быть Мудрец (id=3)"
        print("✅ Правильно!")
    else:
        print("⚠️ Сбалансированный профиль (несколько лидеров)")
    
    ТЕСТ 4: Все архетипы
    print("\n--- ТЕСТ 4: Все архетипы с баллами ---")
    all_arch = get_all_archetypes_with_scores(scores_1, archetypes_mock)
    for arch, score in all_arch:
        if score > 0:
            print(f"  {arch['name']}: {score} баллов")
    
    ТЕСТ 5: ГРАНИЧНЫЙ СЛУЧАЙ — Все одинаковые баллы
    print("\n--- ТЕСТ 5: ГРАНИЧНЫЙ — Все архетипы по 3 балла ---")
    scores_equal = {i: 3 for i in range(1, 9)}
    scores_equal.update({i: 0 for i in range(9, 13)})
    
    primary_equal = get_primary_archetype(scores_equal, archetypes_mock)
    profile_type = analyze_profile_type(scores_equal)
    interpretation = get_interpretation(profile_type, primary_equal[0])
    
    print(f"Баллы: {scores_equal}")
    print(f"Тип профиля: {profile_type}")
    print(f"Интерпретация: {interpretation}")
    assert profile_type == "balanced", "Должен быть сбалансированный профиль"
    print("✅ Правильно обработан!")
    
    ТЕСТ 6: ГРАНИЧНЫЙ — Один явный лидер (9 баллов)
    print("\n--- ТЕСТ 6: ГРАНИЧНЫЙ — Один лидер с 9 баллами ---")
    scores_focused = {3: 9, 5: 3, 7: 3, 2: 3, 11: 3, 6: 3, 1: 0, 4: 0, 8: 0, 9: 0, 10: 0, 12: 0}
    
    primary_focused = get_primary_archetype(scores_focused, archetypes_mock)
    profile_type_focused = analyze_profile_type(scores_focused)
    interpretation_focused = get_interpretation(profile_type_focused, primary_focused[0])
    
    print(f"Баллы: {scores_focused}")
    print(f"Тип профиля: {profile_type_focused}")
    print(f"Интерпретация: {interpretation_focused}")
    assert profile_type_focused == "focused", "Должен быть сфокусированный профиль"
    print("✅ Правильно обработан!")
    
    ТЕСТ 7: ГРАНИЧНЫЙ — Разнообразный профиль
    print("\n--- ТЕСТ 7: ГРАНИЧНЫЙ — Разнообразный (2-3 лидера) ---")
    scores_diverse = {3: 6, 5: 6, 7: 6, 2: 3, 11: 3, 6: 0, 1: 0, 4: 0, 8: 0, 9: 0, 10: 0, 12: 0}
    
    primary_diverse = get_primary_archetype(scores_diverse, archetypes_mock)
    profile_type_diverse = analyze_profile_type(scores_diverse)
    interpretation_diverse = get_interpretation(profile_type_diverse, primary_diverse[0])
    
    print(f"Баллы: {scores_diverse}")
    print(f"Тип профиля: {profile_type_diverse}")
    print(f"Интерпретация: {interpretation_diverse}")
    assert profile_type_diverse == "diverse", "Должен быть разнообразный профиль
    print("✅ Правильно обработан!")
    
    print("\n" + "=" * 60)
    print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
    print("=" * 60)
