import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar

# 读取CSV文件
csv_file = "D:/datas/模型_top300-2.csv"
df = pd.read_csv(csv_file)

# 提取系列为MG、RG、HG、PG的数据
selected_series = ['MG', 'RG', 'HG', 'PG']
selected_df = df[df['系列'].isin(selected_series)].copy()  # 使用copy创建DataFrame的副本

# 创建柱状图
bar = (
    Bar()
    .add_xaxis(selected_series)
    .add_yaxis("平均评分", selected_df.groupby('系列')['评分'].mean().tolist())
    .set_global_opts(
        title_opts=opts.TitleOpts(title="MG、RG、HG、PG四个系列平均评分比较"),
        xaxis_opts=opts.AxisOpts(type_="category", name="系列"),
        yaxis_opts=opts.AxisOpts(type_="value", name="平均评分"),
    )
)

# 渲染为HTML文件
bar.render("mg_rg_hg_pg_avg_rating_bar.html")
