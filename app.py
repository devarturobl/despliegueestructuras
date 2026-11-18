import os
import random

from nicegui import ui


ELEMENT_COUNT = 20
PALETTE = ['#171717', '#2d2d2d', '#444444', '#5b5b5b', '#727272']
values = [random.randint(15, 100) for _ in range(ELEMENT_COUNT)]
labels = [f'Elemento {index:02d}' for index in range(1, ELEMENT_COUNT + 1)]
short_labels = [f'{index:02d}' for index in range(1, ELEMENT_COUNT + 1)]


def radar_options() -> dict:
    return {
        'tooltip': {'trigger': 'item'},
        'radar': {
            'indicator': [{'name': label, 'max': 100} for label in short_labels],
            'radius': '68%',
            'axisName': {'color': '#d4d4d4', 'fontSize': 10},
            'axisLine': {'lineStyle': {'color': 'rgba(255, 255, 255, .22)'}},
            'splitLine': {'lineStyle': {'color': 'rgba(255, 255, 255, .18)'}},
            'splitArea': {'areaStyle': {'color': ['rgba(255, 255, 255, .025)', 'rgba(255, 255, 255, .06)']}},
        },
        'series': [{
            'name': 'Valores',
            'type': 'radar',
            'data': [{
                'name': 'Conjunto actual',
                'value': values,
                'areaStyle': {'color': 'rgba(255, 255, 255, .16)'},
                'lineStyle': {'color': '#f5f5f5', 'width': 2},
                'itemStyle': {'color': '#a3a3a3'},
            }],
        }],
    }


def treemap_options() -> dict:
    groups = [
        {
            'name': f'Grupo {chr(65 + group_index)}',
            'children': [
                {'name': labels[index], 'value': values[index]}
                for index in range(group_index * 5, group_index * 5 + 5)
            ],
        }
        for group_index in range(4)
    ]
    return {
        'tooltip': {
            'formatter': '{b}: {c} unidades',
        },
        'series': [{
            'name': 'Elementos',
            'type': 'treemap',
            'data': groups,
            'roam': False,
            'breadcrumb': {'show': False},
            'visibleMin': 8,
            'label': {'show': True, 'color': '#f8fafc', 'fontSize': 11, 'formatter': '{b}'},
            'upperLabel': {'show': True, 'height': 24, 'color': '#e2e8f0', 'fontWeight': 'bold'},
            'itemStyle': {'borderColor': '#171717', 'borderWidth': 3, 'gapWidth': 3},
            'levels': [
                {},
                {
                    'color': PALETTE,
                    'colorSaturation': [0.35, 0.65],
                    'itemStyle': {'borderColor': '#171717', 'borderWidth': 3, 'gapWidth': 3},
                },
            ],
        }],
    }


def scatter_options() -> dict:
    return {
        'tooltip': {'trigger': 'axis'},
        'grid': {'left': 48, 'right': 22, 'top': 28, 'bottom': 42},
        'xAxis': {
            'type': 'value',
            'name': 'Elemento',
            'nameTextStyle': {'color': '#a3a3a3'},
            'axisLabel': {'color': '#a3a3a3'},
            'axisLine': {'lineStyle': {'color': '#737373'}},
            'splitLine': {'show': False},
        },
        'yAxis': {
            'type': 'value',
            'name': 'Valor',
            'nameTextStyle': {'color': '#a3a3a3'},
            'axisLabel': {'color': '#a3a3a3'},
            'axisLine': {'show': False},
            'splitLine': {'lineStyle': {'color': 'rgba(255, 255, 255, .13)'}},
        },
        'series': [{
            'name': 'Valor',
            'type': 'scatter',
            'data': [[index + 1, value] for index, value in enumerate(values)],
            'symbolSize': 13,
            'itemStyle': {'color': '#e5e5e5', 'borderColor': '#525252', 'borderWidth': 1},
            'emphasis': {'scale': 1.5},
        }],
    }


ui.add_head_html('''
<style>
    body {
        margin: 0;
        background:
            radial-gradient(ellipse at 12% 0%, rgba(14, 116, 144, .22), transparent 38%),
            radial-gradient(ellipse at 90% 15%, rgba(124, 58, 237, .16), transparent 34%),
            #0b1220;
        color: #e2e8f0;
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    .dashboard { max-width: 1440px; margin: 0 auto; padding: 34px 32px 48px; }
    .topbar { display: flex; justify-content: space-between; align-items: center; gap: 20px; }
    .eyebrow { color: #5eead4; font-size: 12px; font-weight: 750; letter-spacing: .12em; text-transform: uppercase; }
    .page-title { color: #f1f5f9; font-size: 30px; font-weight: 750; letter-spacing: -.04em; line-height: 1.15; }
    .page-subtitle { color: #94a3b8; font-size: 14px; margin-top: 6px; }
    .refresh-button { border-radius: 10px; font-weight: 650; padding: 9px 16px; background: #0f766e !important; }
    .metrics { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px; }
    .metric-card, .chart-card {
        background: rgba(17, 28, 47, .88);
        border: 1px solid rgba(148, 163, 184, .14);
        border-radius: 16px;
        box-shadow: 0 12px 30px rgba(0, 0, 0, .14);
    }
    .metric-card { padding: 19px 21px; min-height: 94px; }
    .metric-label { color: #94a3b8; font-size: 12px; font-weight: 600; }
    .metric-value { color: #f1f5f9; font-size: 25px; font-weight: 740; margin-top: 7px; }
    .charts-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px; }
    .chart-card { min-width: 0; padding: 21px 22px 14px; }
    .chart-card--wide { grid-column: 1 / -1; }
    .chart-title { color: #e2e8f0; font-size: 16px; font-weight: 700; }
    .chart-caption { color: #94a3b8; font-size: 12px; margin-top: 4px; }
    .chart-card .q-card, .chart-card .nicegui-chart { width: 100%; }
    @media (max-width: 760px) {
        .dashboard { padding: 24px 16px 36px; }
        .topbar { align-items: flex-start; flex-direction: column; }
        .metrics { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }
        .charts-grid { grid-template-columns: 1fr; }
        .chart-card--wide { grid-column: auto; }
        .chart-card { padding: 17px 14px 10px; }
        .page-title { font-size: 26px; }
    }
</style>
''')

ui.label('Esta app tiene cambios').classes('eyebrow')

@ui.refreshable
def dashboard() -> None:
    total = sum(values)
    average = total / ELEMENT_COUNT

    with ui.column().classes('dashboard w-full gap-6'):
        with ui.row().classes('topbar w-full'):
            with ui.column().classes('gap-0'):
                ui.label('PANEL DE DATOS').classes('eyebrow')
                ui.label('Explorador de valores').classes('page-title')
                ui.label('Una vista nocturna e interactiva de 20 elementos generados al azar.').classes('page-subtitle')
            ui.button(
                'Nuevos datos',
                icon='autorenew',
                on_click=regenerate_data,
            ).props('unelevated no-caps').classes('refresh-button')

        with ui.element('section').classes('metrics'):
            metric('Elementos', f'{ELEMENT_COUNT}', 'dataset')
            metric('Suma total', f'{total:,}', 'functions')
            metric('Promedio', f'{average:.1f}', 'show_chart')
            metric('Valor máximo', f'{max(values)}', 'north_east')

        with ui.element('section').classes('charts-grid'):
            with ui.element('article').classes('chart-card chart-card--wide'):
                ui.label('Perfil de valores').classes('chart-title')
                ui.label('Gráfico radar · compara el conjunto completo de un vistazo').classes('chart-caption')
                ui.echart(radar_options()).style('width: 100%; height: 370px;')

            with ui.element('article').classes('chart-card'):
                ui.label('Composición por grupos').classes('chart-title')
                ui.label('Treemap · el área de cada bloque representa su valor').classes('chart-caption')
                ui.echart(treemap_options()).style('width: 100%; height: 310px;')

            with ui.element('article').classes('chart-card'):
                ui.label('Relación elemento / valor').classes('chart-title')
                ui.label('Dispersión · cada punto representa un elemento').classes('chart-caption')
                ui.echart(scatter_options()).style('width: 100%; height: 310px;')


def metric(title: str, value: str, icon: str) -> None:
    with ui.element('article').classes('metric-card'):
        with ui.row().classes('w-full items-center justify-between no-wrap'):
            with ui.column().classes('gap-0'):
                ui.label(title).classes('metric-label')
                ui.label(value).classes('metric-value')
            ui.icon(icon).classes('text-emerald-300 text-xl')


def regenerate_data() -> None:
    global values
    values = [random.randint(15, 100) for _ in range(ELEMENT_COUNT)]
    dashboard.refresh()


dashboard()
if __name__ in {"__main__", "__mp_main__"}:
    # Lee el puerto que asigna la nube (por defecto 10000 si corres local)
    port = int(os.environ.get('PORT', 10000))
    ui.run(port=port, host='0.0.0.0', storage_secret='un_secreto_seguro')