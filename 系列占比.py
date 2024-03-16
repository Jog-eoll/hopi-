import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Pie

# 读取CSV文件
csv_file = "D:/datas/模型_top300-1.csv"
df = pd.read_csv(csv_file)

# 统计各个系列的数量
series_counts = df['系列'].value_counts()

# 将统计结果转换为pyecharts需要的格式
data = []
for series, count in series_counts.items():
    data.append((series, count))

# 创建饼图
pie = (
    Pie()
    .add(
        "",
        data,
        radius=["40%", "75%"],
        center=["50%", "50%"],
        rosetype="radius",
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="系列占比饼图"),
        legend_opts=opts.LegendOpts(
            orient="vertical", pos_top="15%", pos_left="2%"
        ),
    )
    .set_series_opts(
        tooltip_opts=opts.TooltipOpts(formatter="{a}: {d}%"),
        label_opts=opts.LabelOpts(formatter="{b}: {d}%"),
    )
)

# 生成HTML文件
pie.render("series_pie_chart.html")
