import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar

# 读取CSV文件
csv_file = "D:/datas/模型_top300-2.csv"
df = pd.read_csv(csv_file)

# 提取系列为MG、HG、PG、RG的数据
selected_series = ['MG', 'HG', 'PG', 'RG']
selected_df = df[df['系列'].isin(selected_series)].copy()  # 使用copy创建DataFrame的副本

# 提取出荷时间的年份
selected_df['出荷时间'] = pd.to_datetime(selected_df['出荷时间'], format='%Y').dt.year

# 清理定价列中的数据，将无法转换为数字的值替换为NaN
selected_df['定价'] = pd.to_numeric(selected_df['定价'], errors='coerce')

# 创建柱状图
bar = (
    Bar()
    .add_xaxis(selected_df['出荷时间'].unique().tolist())
    .set_global_opts(
        title_opts=opts.TitleOpts(title="MG、HG、PG、RG系列每年平均定价统计"),
        xaxis_opts=opts.AxisOpts(type_="category", name="年份"),
        yaxis_opts=opts.AxisOpts(type_="value", name="平均定价（日元）"),
    )
)

# 添加柱状图数据
for series in selected_series:
    series_data = selected_df[selected_df['系列'] == series].groupby('出荷时间')['定价'].mean().tolist()
    bar.add_yaxis(series, series_data)

# 渲染为HTML文件
bar.render("mg_hg_pg_rg_avg_price_bar.html")
