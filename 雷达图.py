import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Radar, Page

# 读取CSV文件
data = pd.read_csv("D:/datas/模型_top300-2.csv")

# 选择需要的列
selected_columns = ['系列', '定价', '评分', '参考价格', '现价']
data = data[selected_columns]
print(data)
# 将列数据转换为数值型，处理非数值数据为NaN
data = data.apply(pd.to_numeric, errors='coerce')

# 删除包含NaN的行
data = data.dropna()

# 按照系列分组，计算每个系列的平均值
series_data = data.groupby('系列').mean().reset_index()

# 创建雷达图
def create_radar(series_name, data_values, max_value) -> Radar:
    c = (
        Radar()
        .add_schema(
            schema=[
                opts.RadarIndicatorItem(name="平均定价", max_=max_value),
                opts.RadarIndicatorItem(name="平均评分", max_=max_value),
                opts.RadarIndicatorItem(name="平均参考价格", max_=max_value),
                opts.RadarIndicatorItem(name="平均现价", max_=max_value),
            ]
        )
        .add(
            series_name,
            [data_values.tolist()],
            linestyle_opts=opts.LineStyleOpts(color="blue"),
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(title=f"{series_name} 系列雷达图"),
            legend_opts=opts.LegendOpts(selected_mode="single"),
        )
    )
    return c

# 创建 Page 对象，包含所有雷达图
page = Page()
max_value = data.max().max()  # 获取数据中的最大值
for index, row in series_data.iterrows():
    radar_chart = create_radar(row['系列'], row.drop('系列'), max_value)
    page.add(radar_chart)

# 保存为 HTML 文件
page.render("radar_charts.html")
