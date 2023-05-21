import pandas as pd
from plotly import express as px
from scipy import stats
from statsmodels.stats.multitest import multipletests


def significant_metabolites(data: pd.DataFrame) -> pd.DataFrame:
    features = data.drop('Group', axis=1)
    show=[]
    col=[]
    if data['Group'].nunique() > 2:
        for column in features.columns:
            values = {group: values.fillna("median").values for group, values in data.groupby(data['Group'])[column]}
            pvalue=stats.kruskal(*list(values.values()))[1]
            if pvalue < 0.05:
                show.append(pvalue)
                col.append(column)
        p_adjusted = multipletests(show, alpha=0.05, method='bonferroni')
        df=pd.DataFrame({'Metabolite':col, 'p-value':show, 'p-value with bonferroni corr':p_adjusted[1]})
        df=df.sort_values(by='p-value with bonferroni corr')
    else:
        for column in features.columns:
            data1=data[data['Group']==data['Group'].unique()[0]][column]
            #data1 = data1.drop('Group', axis=1)
            data1=data1.fillna(data1.median())
            data2=data[data['Group']==data['Group'].unique()[1]][column]
            #data2 = data2.drop('Group', axis=1)
            data2=data2.fillna(data2.median())
            pvalue=stats.mannwhitneyu(data1, data2)[1]
            if pvalue < 0.05:
                show.append(pvalue)
                col.append(column)
            df=pd.DataFrame({'Metabolite':col, 'p-value':show})
            p_adjusted = multipletests(show, alpha=0.05, method='bonferroni')
            df = pd.DataFrame({'Metabolite': col, 'p-value': show, 'p-value with bonferroni corr': p_adjusted[1]})
            df = df.sort_values(by='p-value with bonferroni corr')
    return df


def create_graphs(df: pd.DataFrame):
    """Функция для создания графиков из таблицы
    Создание пустого словаря для хранения графиков"""
    graphs = {}
    # Перебор всех столбцов в таблице
    for col in df.columns:
        # Пропуск первого столбца с метками класса
        if col == 'Group':
            continue
        # Создание графика боксплота для каждого столбца
        fig = px.box(df, x='Group', y=col)
        # Сохранение графика в словарь
        graphs[col] = fig.to_html()
    # Возврат словаря с графиками
    return graphs
