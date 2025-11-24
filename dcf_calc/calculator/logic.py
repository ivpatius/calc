# calculator/logic.py
import math


def _num(value, default=0.0):
    """
    Вспомогательная функция: безопасно переводит значение в float.
    Пустое значение -> default.
    """
    if value in (None, ''):
        return default
    return float(value)


def compute_dcf(data: dict) -> dict:
    """
    Основные формулы:

    1) FCF = EBIT * (1 - T_oper) + Амортизация - CAPEX - ΔWC

    2) Re (CAPM + премии):
       Re_base = Rf + β * (Rm - Rf)
       Re = Re_base + Premium_small + Premium_country

    3) WACC:
       V = E + D (или Capital, если задан)
       WACC = (E/V) * Re + (D/V) * Rd * (1 - T)

    4) Терминальная стоимость (по Гордону):
       TV = FCF_{n+1} / (WACC - g),
       где FCF_{n+1} = FCF * (1 + g)

    5) Приведение к текущему моменту:
       PV_FCF = FCF * (1 - (1 + WACC)^(-n)) / WACC   (аннуитет)
       PV_TV = TV / (1 + WACC)^n

       EV = PV_FCF + PV_TV
       (при mid-year корректировке — дополнительное деление на sqrt(1 + WACC))

    6) Стоимость собственного капитала:
       Equity_value = EV - NetDebt - Minority + NonOperatingAssets

       Цена акции = Equity_value / Shares
    """

    # ---- Шаг 1: FCF ----
    ebit = _num(data.get('ebit'))
    tax_rate_oper = _num(data.get('tax_rate_oper')) / 100.0  # в долях
    depr = _num(data.get('depr'))
    capex = _num(data.get('capex'))
    wc_change = _num(data.get('wc_change'))
    periods = int(_num(data.get('periods'), 1)) or 1
    not_from_beginning = bool(data.get('not_from_beginning'))

    ebit_after_tax = ebit * (1 - tax_rate_oper)
    fcf = ebit_after_tax + depr - capex - wc_change

    # ---- Шаг 2: Re и WACC ----
    rf = _num(data.get('rf')) / 100.0
    market_return = _num(data.get('market_return')) / 100.0
    project_risk = _num(data.get('project_risk'))
    small_business_risk = _num(data.get('small_business_risk')) / 100.0
    country_risk = _num(data.get('country_risk')) / 100.0

    market_premium = max(market_return - rf, 0.0)
    re_capm = rf + project_risk * market_premium
    re = re_capm + small_business_risk + country_risk  # уже в долях

    equity = _num(data.get('equity'))
    capital = _num(data.get('capital'))
    debt = _num(data.get('debt'))
    rd = _num(data.get('rd')) / 100.0
    tax_rate = _num(data.get('tax_rate')) / 100.0

    V = capital if capital > 0 else (equity + debt)

    if V <= 0:
        wacc = re  # fallback: считаем, что WACC = Re
        e_share = 1.0
        d_share = 0.0
    else:
        e_share = equity / V
        d_share = debt / V
        wacc = e_share * re + d_share * rd * (1 - tax_rate)

    # ---- Шаг 3: TV ----
    g = _num(data.get('growth_rate')) / 100.0
    if wacc <= g or wacc <= 0:
        tv = 0.0
    else:
        tv = fcf * (1 + g) / (wacc - g)

    # ---- Дисконтирование потоков ----
    if wacc <= 0:
        pv_fcf = fcf * periods
        pv_tv = tv  # без дисконтирования, если wacc не задан адекватно
    else:
        pv_fcf = fcf * (1 - (1 + wacc) ** (-periods)) / wacc
        discount_factor = (1 + wacc) ** periods
        pv_tv = tv / discount_factor

    ev = pv_fcf + pv_tv

    # mid-year корректировка (если проект стартует не с начала года)
    if not_from_beginning and wacc > -1:
        mid_coeff = 1.0 / math.sqrt(1 + wacc)
        pv_fcf *= mid_coeff
        pv_tv *= mid_coeff
        ev = pv_fcf + pv_tv

    # ---- Шаг 4: переход к Equity ----
    net_debt = _num(data.get('net_debt'))
    minority = _num(data.get('minority'))
    non_operating_assets = _num(data.get('non_operating_assets'))

    equity_value = ev - net_debt - minority + non_operating_assets

    # ---- Шаг 5: цена акции ----
    shares = _num(data.get('shares'))
    implied_price = equity_value / shares if shares > 0 else None

    # Возвращаем всё, что может пригодиться для вывода
    return {
        'ebit_after_tax': ebit_after_tax,
        'fcf': fcf,
        're_percent': re * 100,
        'wacc_percent': wacc * 100,
        'tv': tv,
        'pv_fcf': pv_fcf,
        'pv_tv': pv_tv,
        'ev': ev,
        'equity_value': equity_value,
        'implied_price': implied_price,
        'periods': periods,
        'g_percent': g * 100,
    }
