import pickle

import matplotlib.pyplot as plt
import pandas as pd


def display_plot(bus_number,weekday = True, timing = False, busstop = False):
    if weekday:
        weekday_print = "Weekday"
        processed_file = open("app/aggregate_pickles/segment/aggregate_usage_processed_weekday.p","rb")
    else:
        weekday_print = "Weekend"
        processed_file = open("app/aggregate_pickles/segment/aggregate_usage_processed_weekend.p","rb")

    processed = pickle.load(processed_file)
    processed_file.close()

    small = processed[str(bus_number)]
    counter = 0
    empty = True
    if small[0].Direction.value_counts().count() == 1: #need to rework this part
        while True:
            try:
                test = pd.DataFrame(columns = ["time","usage"])
                for i in small:
                    test.loc[i] = [i,small[i].iloc[counter].Usage]
                if (test["usage"]!=0).any():
                    empty = False
                plt.plot(test["time"],test["usage"],color='y')
                if timing:
                    test.loc[test.index>int(timing),'usage'].plot(color='r')
                counter += 1
            except:
                break
    else:
        direction = small[0][small[0]["FromBusStop"] == busstop].Direction
        number = small[0]
        number_idx = number[number["ToBusStop"] == busstop].index[0]
        number_stops = number.iloc[number_idx:].Link.count()
        total_number_stops = small[0][small[0]["Direction"]==direction.values[0]].Link.count()
        alpha_counter = 0
        while True:
            try:
                alpha = 0.1
                color = "k"
                test = pd.DataFrame(columns = ["time","usage"])
                
                for i in small:
                    test.loc[i] = [i,small[i][small[i]["Direction"]==direction.values[0]].iloc[counter].Usage]
                
                if (test["usage"]!=0).any():
                    empty = False
                
                if total_number_stops < number_stops:
                    a = test.loc[test.index <= int(timing),'usage'].to_frame()
                    plt.plot(a.index,a["usage"],color='y', alpha = alpha)
                    a = test.loc[test.index >= int(timing),'usage'].to_frame()
                    alpha = 1 - 1/number_stops*alpha_counter
                    alpha_counter += 1
                    color = "r"
                    plt.plot(a.index,a["usage"],color=color, alpha = alpha)
                    
                counter += 1
                total_number_stops -= 1
            except:
                break
    plt.xlabel("Time")
    plt.ylabel("Usage Count")
    plt.title("Bus {} {}".format(bus_number,weekday_print))
    if empty:
        return False
    return True
