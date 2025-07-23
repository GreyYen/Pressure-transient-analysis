
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import lasio

def load_csv(path):
    return pd.read_csv(path)

def load_las(path):
    las = lasio.read(path)
    data = pd.DataFrame({
        'time': las.data[:, 0],
        'pressure': las.data[:, 1]
    })
    return data

def plot_pressure(data, save_path):
    time = data['time']
    pressure = data['pressure']

    dlogt = np.gradient(np.log10(time))
    dlogp = np.gradient(pressure, dlogt)
    derivative = dlogp * time / np.gradient(time)

    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.loglog(time, pressure)
    plt.title("Pressure vs Time")
    plt.xlabel("Time (hr)")
    plt.ylabel("Pressure (psi)")
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.loglog(time, derivative, color='orange')
    plt.title("Pressure Derivative vs Time")
    plt.xlabel("Time (hr)")
    plt.ylabel("dP/dln(t)")
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def run_analysis():
    os.makedirs("plots", exist_ok=True)
    data = load_csv("data/pressuredataset.csv")
    plot_pressure(data, "plots/pressure_transient_plot.png")
