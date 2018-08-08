import pickle
import pandas as pd

def get_bus_description(bus_stop_code):
    data = pd.read_json("app/aggregate_pickles/stops.json")
    return data[data["BusStopCode"] == "{:05d}".format(int(bus_stop_code))].Description.values[0]

def bus_available(bus_number):
    return bus_number in pd.read_pickle("app/aggregate_pickles/segment/aggregate_usage.p").keys()

def get_busstop_rankings(weekday=True):
    if weekday:
        test = pd.read_csv("app/aggregate_pickles/busstop/busstop_aggregate_usage_weekday.csv",index_col = 0)
    else:
        test = pd.read_csv("app/aggregate_pickles/busstop/busstop_aggregate_usage_weekend.csv",index_col = 0)
    test1 = test.dropna()
    test2 = test1.groupby("bus_stop").sum()[["board_count","alight_count"]]
    test3 = test2.nlargest(10,"board_count")
    return [[get_bus_description(i)] + [int(sum(test3.loc[i].tolist()))] for i in test3.index]


def get_segment_rankings(weekday = True):
    if weekday:
        segment_file = open("app/aggregate_pickles/segment/segment_rankings_weekday.p","rb")
    else:
        segment_file = open("app/aggregate_pickles/segment/segment_rankings_weekend.p","rb")
    data = pickle.load(segment_file)
    segment_file.close()
    return [["{} to {}".format(get_bus_description(i[0].split("_")[0]),get_bus_description(i[0].split("_")[1]))]+[int(i[1])] for i in data[:10]]


def get_busservice_rankings(weekday=True):
    if weekday:
        segment_file = open("app/aggregate_pickles/bus_ranking/bus_service_rankings_weekday.p","rb")
    else:
        segment_file = open("app/aggregate_pickles/bus_ranking/bus_service_rankings_weekend.p","rb")
    data = pickle.load(segment_file)
    segment_file.close()
    return [[int(i[0])]+[int(i[1])] for i in data[-10:]]