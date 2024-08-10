from unittest.mock import patch
from tech_news.analyzer.reading_plan import ReadingPlanService
import pytest


def test_reading_plan_group_news():
    # Cenário de exemplo: notícias fictícias
    mock_data_1 = [
        {"title": "Notícia 1", "reading_time": 8},
        {"title": "Notícia 2", "reading_time": 10},
        {"title": "Notícia 3", "reading_time": 15},
        {"title": "Notícia 4", "reading_time": 12},
    ]

    # Resultados esperados
    expected_result_1 = {
        "readable": [
            {
                "unfilled_time": 2,
                "chosen_news": [
                    ("Notícia 1", 8),
                ],
            },
            {
                "unfilled_time": 0,
                "chosen_news": [
                    ("Notícia 2", 10),
                ],
            },
        ],
        "unreadable": [
            ("Notícia 3", 15),
            ("Notícia 4", 12),
        ],
    }

    # Teste com notícias que se encaixam em 10 minutos
    with patch(
        "tech_news.analyzer.reading_plan.ReadingPlanService._db_news_proxy",
        return_value=mock_data_1,
    ):
        result = ReadingPlanService.group_news_for_available_time(10)
        assert result == expected_result_1

    # Teste com notícias que não podem ser lidas no tempo disponível
    mock_data_2 = [
        {"title": "Notícia 1", "reading_time": 50},
        {"title": "Notícia 2", "reading_time": 75},
    ]

    expected_result_2 = {
        "readable": [],
        "unreadable": [
            ("Notícia 1", 50),
            ("Notícia 2", 75),
        ],
    }

    with patch(
        "tech_news.analyzer.reading_plan.ReadingPlanService._db_news_proxy",
        return_value=mock_data_2,
    ):
        result = ReadingPlanService.group_news_for_available_time(30)
        assert result == expected_result_2

    # Teste com todas as notícias legíveis no tempo disponível
    mock_data_3 = [
        {"title": "Notícia 1", "reading_time": 12},
        {"title": "Notícia 2", "reading_time": 6},
    ]

    expected_result_3 = {
        "readable": [
            {
                "unfilled_time": 2,
                "chosen_news": [
                    ("Notícia 1", 12),
                    ("Notícia 2", 6),
                ],
            },
        ],
        "unreadable": [],
    }

    with patch(
        "tech_news.analyzer.reading_plan.ReadingPlanService._db_news_proxy",
        return_value=mock_data_3,
    ):
        result = ReadingPlanService.group_news_for_available_time(20)
        assert result == expected_result_3

    # Teste com valor de tempo inválido
    with pytest.raises(
        ValueError, match="Valor 'available_time' deve ser maior que zero"
    ):
        ReadingPlanService.group_news_for_available_time(0)
