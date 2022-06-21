import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from pathlib import Path
import numpy as np
import pandas as pd
import subprocess
import tomli
import tomli_w


def get_csv():
    """Establish connection with raspi and pull csv"""

    file_path = Path.cwd()
    remote_file_location = "pi@192.168.0.38:/home/pi/speedtest/speedtest.csv"
    local_file_location = file_path.joinpath('data', 'speedtest.csv')
    command = ["scp", remote_file_location, local_file_location]
    subprocess.run(command)

def panda_csv():
    """ Get data from csv """

    file_path = Path.cwd()
    local_file_location = file_path.joinpath('data', 'speedtest.csv')
    columns = ["DateTime", "Ping (ms)", "Jitter (ms)", "Download (Mbps)", "Upload (Mbps)"]
    df = pd.read_csv(local_file_location, usecols=columns)
    return df

def convert_to_np_array(df):
    "Converts what it expects to be a pandas dataframe (but an be anything) into a numpy array"

    np_array = np.asarray(df)
    return np_array

def my_plotter(data1, data2, param_dict={}, xlabel='', ylabel='', title=''):
    """ A helper function to make a single graph """

    fig, ax = plt.subplots()
    
    ax.set_xlabel(str(xlabel))
    ax.set_ylabel(str(ylabel))
    ax.set_title(str(title))
    ax.xaxis.set_major_locator(ticker.AutoLocator())
    ax.tick_params(axis='x', rotation=45)
    
    out = ax.plot(data1, data2, **param_dict)

    return out

def read_from_config():
    p = Path.cwd()
    with open(str(p) + "/src/network_warden/config.toml", "rb") as f:
        toml_dict = tomli.load(f)
    
    return toml_dict

def edit_config(section, key, new_value):
    current_config = read_from_config()
    current_config[section][key] = new_value
    p = Path.cwd()
    with open(str(p) + "/src/network_warden/config.toml", "wb") as f:
        tomli_w.dump(current_config, f)