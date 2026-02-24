Тест "Какой вы архетип?"

Структура:
Загрузка статичных данных (JSON)
Управление состоянием (session_state)
Показ вопросов (один за одним)
Подсчёт баллов (scoring.py)
Визуализация результата (visualization.py)


import streamlit as st
import json
import sys
from pathlib import Path

Добавить папку src в путь для импорта модулей
sys.path.append(str(Path(__file__).parent / "src"))

Импорт модулей
from scoring import (
    calculate_scores,
    get_top_3_archetypes,
    get_all_archetypes_with_scores,
    scores_to_percentages,
    analyze_profile_type
)

from visualization import (
    apply_custom_styles,
    show_test_header,
    show_start_button,
    show_question_with_options,
    display_result,
    show_restart_button
)


КОНФИГУРАЦИЯ

st.set_page_config(
    page_title="🎭 Тест: Какой вы архетип?",
    page_icon="🎭",
    layout="centered",
    initial_sidebar_state="collapsed"
)


ЗАГРУЗКА ДАННЫХ

@st.cache_data
def load_json_data():
    
    Загружает СТАТИЧНЫЕ данные из JSON файлов
    
    Возвращает:
        Кортеж (archetypes_data, questions_data)
  
    try:
        Загрузить архетипы
        with open("data/archetypes.json", "r", encoding="utf-8") as f:
            archetypes_data = json.load(f)
        
        Загрузить вопросы
        with open("data/questions.json", "r", encoding="utf-8") as f:
            questions_data = json.load(f)
        
        return archetypes_data, questions_data
    
    except FileNotFoundError as e:
        st.error(f"❌ Файл не найден: {e}")
        st.stop()
    
    except json.JSONDecodeError as e:
        st.error(f"❌ Ошибка в JSON файле: {e}")
        st.stop()


ИНИЦИАЛИЗАЦИЯ СОСТОЯНИЯ 

def init_session_state():
    
    Инициализирует session_state для управления тестом
    
    if 'test_started' not in st.session_state:
        st.session_state.test_started = False
    
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = []
    
    if 'test_finished' not in st.session_state:
        st.session_state.test_finished = False


ЛОГИКА ТЕСТА 

def handle_answer_selection(selected_option_index):
    
    Обрабатывает выбор ответа пользователем
    
    Параметры:
        selected_option_index: индекс выбранного варианта (0, 1, 2)
    
    Сохранить ответ
    st.session_state.user_answers.append(selected_option_index)
    
    Перейти к следующему вопросу
    st.session_state.current_question += 1
    
    Проверить, закончился ли тест
    total_questions = 8
    if st.session_state.current_question >= total_questions:
        st.session_state.test_finished = True
    
    Перерисовать страницу
    st.rerun()


def show_current_question(questions_data):
    Показывает текущий вопрос пользователю
    
    Параметры:
        questions_data: данные из questions.json
    current_idx = st.session_state.current_question
    total_questions = len(questions_data['questions'])
    
    Получить данные текущего вопроса
    question_data = questions_data['questions'][current_idx]
    
    Показать вопрос через visualization.py
    selected_option = show_question_with_options(
        question_data,
        question_number=current_idx + 1,
        total_questions=total_questions
    )
    
    Если пользователь выбрал вариант
    if selected_option is not None:
        handle_answer_selection(selected_option)


def calculate_and_display_results(archetypes_data, questions_data):
    
    ГЛАВНАЯ ФУНКЦИЯ: Подсчёт баллов и отображение результата
    
    Параметры:
        archetypes_data: данные из archetypes.json
        questions_data: данные из questions.json
    
    ШАГ 1: ПОДСЧЁТ БАЛЛОВ
    scores = calculate_scores(
        st.session_state.user_answers,
        questions_data
    )
    
    ШАГ 2: АНАЛИЗ РЕЗУЛЬТАТОВ 
    Получить топ-3 архетипа
    top_3_list = get_top_3_archetypes(scores, archetypes_data)
    
    Получить все архетипы с баллами
    all_archetypes_list = get_all_archetypes_with_scores(scores, archetypes_data)
    
    Конвертировать баллы в проценты
    percentages = scores_to_percentages(scores)
    
    Определить тип профиля
    profile_type = analyze_profile_type(scores)
    
    ШАГ 3: ВИЗУАЛИЗАЦИЯ
    display_result(
        scores=scores,
        percentages=percentages,
        top_3_list=top_3_list,
        all_archetypes_list=all_archetypes_list,
        profile_type=profile_type
    )
    
    ШАГ 4: КНОПКА "ПРОЙТИ ЗАНОВО"
    show_restart_button()


ГЛАВНАЯ ЛОГИКА

def main():
    ГЛАВНАЯ ФУНКЦИЯ приложения
    
    Порядок работы:
    1. Применить стили
    2. Загрузить данные
    3. Инициализировать состояние
    4. Показать соответствующий экран (старт/вопросы/результат)
    # Применить CSS стили
    apply_custom_styles()
    
    Загрузить данные
    archetypes_data, questions_data = load_json_data()
    
    Инициализировать состояние
    init_session_state()
    
    РЕЖИМ 1: СТАРТОВЫЙ ЭКРАН 
    if not st.session_state.test_started:
        show_test_header()
        show_start_button()
    
    РЕЖИМ 2: ПРОХОЖДЕНИЕ ТЕСТА 
    elif not st.session_state.test_finished:
        show_current_question(questions_data)
    
    РЕЖИМ 3: РЕЗУЛЬТАТЫ 
    else:
        calculate_and_display_results(archetypes_data, questions_data)


ТОЧКА ВХОДА

if __name__ == "__main__":
    main()
