# calculator/forms.py
from django import forms


class DCFForm(forms.Form):
    # Шаг 1 — FCF
    ebit = forms.FloatField(
        label='EBIT',
        required=False
    )
    tax_rate_oper = forms.FloatField(
        label='Налоговая ставка по операционной деятельности, %',
        required=False
    )
    depr = forms.FloatField(
        label='Амортизация',
        required=False
    )
    capex = forms.FloatField(
        label='Капитальные затраты',
        required=False
    )
    wc_change = forms.FloatField(
        label='Изменение оборотного капитала',
        required=False
    )
    periods = forms.IntegerField(
        label='Количество периодов прогноза',
        required=False,
        min_value=1,
        initial=5
    )
    not_from_beginning = forms.BooleanField(
        label='Проект начинается не с начала года',
        required=False
    )

    # Шаг 2 — Re и WACC
    rf = forms.FloatField(
        label='Безрисковая ставка (ОФЗ), %',
        required=False
    )
    market_return = forms.FloatField(
        label='Среднерыночная доходность, %',
        required=False
    )
    project_risk = forms.FloatField(
        label='Коэффициент риска проекта (β)',
        required=False,
        initial=0.5
    )
    small_business_risk = forms.FloatField(
        label='Риск инвестирования в малый бизнес, п.п.',
        required=False
    )
    country_risk = forms.FloatField(
        label='Страновой риск, п.п.',
        required=False
    )

    equity = forms.FloatField(
        label='Собственный капитал (Equity)',
        required=False
    )
    capital = forms.FloatField(
        label='Совокупный капитал (Capital)',
        required=False
    )
    rd = forms.FloatField(
        label='Стоимость долга (Rd), %',
        required=False
    )
    debt = forms.FloatField(
        label='Объём долга',
        required=False
    )
    tax_rate = forms.FloatField(
        label='Ставка налога на прибыль, %',
        required=False
    )

    # Шаг 3 — TV
    growth_rate = forms.FloatField(
        label='Долгосрочная ставка роста (g), %',
        required=False
    )

    # Шаг 4 — EV
    net_debt = forms.FloatField(
        label='Чистый долг',
        required=False
    )
    minority = forms.FloatField(
        label='Неконтролируемые доли',
        required=False
    )
    non_operating_assets = forms.FloatField(
        label='Непрофильные активы',
        required=False
    )

    # Шаг 5 — цена акции
    shares = forms.FloatField(
        label='Количество акций',
        required=False
    )
