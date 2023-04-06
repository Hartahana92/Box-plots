import plotly.graph_objects as go
import pandas as pd
import dash
from dash import html, dcc
# Загрузка данных
df = pd.read_excel('/Users/ksu_/Documents/notebooks/CVD/CVDC/Файлы для ввода/IHD_AMI.xlsx')

# Создание дэшборда
app = dash.Dash()

# Создание графиков
figures = []
for col in df.columns[1:]:
    # Создание боксплота
    box_plot = go.Box(
        x=df['Group'],
        y=df[col],
        name=col
    )
    figures.append(box_plot)
fig = go.Figure(figures)
fig.write_html("figures.html")

# Добавление графиков на дэшборд
app.layout = html.Div([
    dcc.Graph(
        figure={
            'data': figures
        }
    )
])

# Запуск дэшборда
if __name__ == '__main__':
    app.run_server(debug=True)
