# %%

import time
import json
import requests
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Pie, Grid, Map


url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d' % int(time.time() * 1000)
html = requests.get(url)
data = json.loads(html.json()['data'])
china_data = data['areaTree'][0]['children']
data_set = []
for i in china_data:
    data_dict = {}
    data_dict['province'] = i['name']
    data_dict['nowConfirm'] = i['total']['nowConfirm']
    data_dict['confirm'] = i['total']['confirm']
    data_dict['dead'] = i['total']['dead']
    data_dict['heal'] = i['total']['heal']
    data_dict['deadRate'] = i['total']['deadRate']
    data_dict['healRate'] = i['total']['healRate']
    data_set.append(data_dict)
data_set

# %%

df = pd.DataFrame(data_set)
df

# %%

df.to_csv('国内疫情数据.csv')

# %%



# %%

df2 = df.sort_values(by=['nowConfirm'], ascending=False)[:5]
df2

# %%

[list(i) for i in zip(df2['province'].values.tolist(), df2['nowConfirm'].values.tolist())]

# %%

pie = (
    Pie()
        .add(
        "",
        [list(i) for i in zip(df2['province'].values.tolist(), df2['nowConfirm'].values.tolist())],
        radius=["10%", "30%"]
    )
        .set_global_opts(
        legend_opts=opts.LegendOpts(orient="vertical", pos_top="70%", pos_left="70%"),
    )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{c}"))
)
pie.render_notebook()

# %%

line = (
    Line()
        .add_xaxis(list(df['province'].values))
        .add_yaxis("治愈率", df['deadRate'].values.tolist())
        .add_yaxis("死亡率", df['healRate'].values.tolist())
        .set_global_opts(
        title_opts=opts.TitleOpts(title="死亡率与治愈率"),
    )
)
line.render_notebook()

# %%

bar = (
    Bar()
        .add_xaxis(list(df['province'].values)[:6])
        .add_yaxis("死亡", df['dead'].values.tolist()[:6])
        .add_yaxis("治愈", df['heal'].values.tolist()[:6])
        .set_global_opts(
        title_opts=opts.TitleOpts(title="各地区死亡与治愈人数"),
        datazoom_opts=[opts.DataZoomOpts()],
    )
)
bar.render_notebook()

# %%

china_map = (
    Map()
        .add("现有确诊", [list(i) for i in zip(df['province'].values.tolist(), df['nowConfirm'].values.tolist())])
        .set_global_opts(
        title_opts=opts.TitleOpts(title="各地区确诊人数", pos_top="48%", pos_left="65%"),
        visualmap_opts=opts.VisualMapOpts(max_=200, is_piecewise=True),
        legend_opts=opts.LegendOpts(pos_left="90%", pos_top="60%"),
    )
)
china_map.render_notebook()

# %%

grid = (
    Grid(init_opts=opts.InitOpts(width="1600px", height="900px"))
        .add(line, grid_opts=opts.GridOpts(pos_top="60%", pos_right="60%"))
        .add(bar, grid_opts=opts.GridOpts(pos_bottom="60%", pos_right="60%"))
        .add(pie, grid_opts=opts.GridOpts(pos_top="30%", pos_right="30%"))
        .add(china_map, grid_opts=opts.GridOpts(pos_top="60%", pos_right="60%"))
)
grid.render()
grid.render_notebook()
