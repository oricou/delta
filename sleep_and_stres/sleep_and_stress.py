import matplotlib.pyplot as plt
import pandas as pd

def sleep_time_mean_per_stress_level():
    data = pd.read_csv("data/SaYoPillow.csv")
    data = data.sort_values("sl")
    sleep_mean = [data[data["sl"] == i]["sr.1"].mean() for i in range(5)]

    plt.plot(sleep_mean, data["sl"].unique())
    plt.show()

def stress_level_comparaison():
    data = pd.read_csv("data/SaYoPillow.csv")
    data = data.sort_values("sl")
    sr_mean = [data[data["sl"] == i]["sr.1"].mean() for i in range(5)]
    rr_mean = [data[data["sl"] == i]["rr"].mean() for i in range(5)]
    t_mean = [data[data["sl"] == i]["t"].mean() for i in range(5)]
    lm_mean = [data[data["sl"] == i]["lm"].mean() for i in range(5)]
    bo_mean = [data[data["sl"] == i]["bo"].mean() for i in range(5)]
    rem_mean = [data[data["sl"] == i]["rem"].mean() for i in range(5)]
    hr_mean = [data[data["sl"] == i]["hr"].mean() for i in range(5)]


    #plt.plot(data["sl"].unique(),sr_mean)
    #plt.plot(data["sl"].unique(),rr_mean)
    #plt.plot(data["sl"].unique(),t_mean)
    #plt.plot(ldata["sl"].unique(),m_mean)
    #plt.plot(data["sl"].unique(),bo_mean)
    #plt.plot(data["sl"].unique(),rem_mean)
    plt.bar(data["sl"].unique(),hr_mean)

    plt.show()

if __name__ == "__main__":
    stress_level_comparaison()
