import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
matplotlib.rcParams['figure.figsize'] = [15, 9]

df=spark.sql("""select * from tmp.sleep_data_3_2""").toPandas()
print(df.shape)

from tslearn.clustering import TimeSeriesKMeans
from tslearn.datasets import CachedDatasets
from tslearn.preprocessing import TimeSeriesScalerMeanVariance, TimeSeriesResampler
appliance_id_list=set(df["appliance_id"].tolist())
ts_array_all=[]
for i in appliance_id_list:
    sub_df=df[df['appliance_id']==i].iloc[:,2:]
    num = sub_df.shape[0]
    #if num<=10 ---k=1
    #if num>10 ---k=2
    if(num<=10):
        k=1
    else:
        k=2
    ts_array = sub_df.values
    ts_scaled = TimeSeriesScalerMeanVariance().fit_transform(ts_array)
    km = TimeSeriesKMeans(n_clusters=k, metric="dtw",verbose=True, random_state=0)
    y_pred = km.fit_predict(ts_scaled)
#     n=np.argmax(np.bincount(y_pred))

    ts_array_all.append(km.cluster_centers_.ravel())

#找到每个设备的聚类中心后，在对聚类中心做一次聚类
ts_array_all=np.array(ts_array_all)
ts_scaled = TimeSeriesScalerMeanVariance().fit_transform(ts_array_all)
km = TimeSeriesKMeans(n_clusters=6, metric="dtw",verbose=True, random_state=0)
y_pred = km.fit_predict(ts_scaled)
#画图的部分
sample_size=10000#ts_array_all的行数
def get_proportion(y_pred):
    df_y = pd.DataFrame(y_pred, columns=['y'])
    df_p = df_y['y'].groupby(df_y['y']).count()/df_y.shape[0]*100
    return df_p

sample_list = random.sample(range(ts_scaled.shape[0]), sample_size)
ts_sample = ts_scaled[np.array(sample_list)]
y_sample = y_pred[np.array(sample_list)]
df_p = get_proportion(y_pred)
plt.figure()
for yi in range(6):
    ax = plt.subplot(2, 3, yi + 1)
    ax.set_title('cluster k=%d \n proportion = %.1f' %(yi, df_p[yi]))
    for xx in ts_sample[y_sample == yi]:
        plt.plot(xx.ravel(), "k-", alpha=.2, linewidth=0.9)
    plt.plot(km.cluster_centers_[yi].ravel(), "r-", linewidth=2.5)
    plt.xlim(0, 9)
    plt.ylim(-4, 4)
    #if yi == 1:
    #    plt.title("All user profiles and the centre of clusters")
plt.subplots_adjust(hspace = 0.3)
plt.show()