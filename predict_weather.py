import matplotlib.pyplot as plt
import numpy as np

class Predictor(object):
    def __init__(self):
        temps, year, month, day = self.get_data()
        self.temp_calender = self.build_temp_calender(temps, year, month, day)
        deseasonized_temps = np.zeros(temps.size)
        for i, temp in enumerate(temps):
            seasonal_temp = self.find_seasonal_temp(year[i], month[i], day[i])
            deseasonized_temps[i] = temp - seasonal_temp

        self.slope, self.intercept = self.get_three_day_coefficients(deseasonized_temps)

    def get_data(self):
    	filename = 'florida_climate.csv'
    	weather_file = open(filename)
    	weather_data = weather_file.read()
    	weather_file.close()
    	lines = weather_data.split('\n')
    	labels = lines[0]
    	values = lines[1:]
    	n_values = len(values)
    	day = []
    	month = []
    	year = []
    	max_temp = []
    	j_day = 3
    	j_month = 2
    	j_year= 1
    	j_max_temp = 5
    	for i_row in range(n_values):
    		split_values = values[i_row].split(',')
    		if len(split_values)>j_max_temp:
    			day.append(int(split_values[j_day]))
    			month.append(int(split_values[j_month]))
    			year.append(int(split_values[j_year]))
    			max_temp.append(float(split_values[j_max_temp]))
    	i_mid = len(max_temp)//2
    	temps = np.array(max_temp[i_mid:])
    	year = np.array(year[i_mid:])
    	month = np.array(month[i_mid:])
    	day = np.array(day[i_mid:])
    	temps[np.where(temps==-99.9)] = np.nan
    	i_start = np.where(np.logical_not(np.isnan(temps)))[0][0]
    	temps = temps[i_start:]
    	year = year[i_start:]
    	month =month[i_start:]
    	day = day[i_start:]
    	for i in range(temps.size):
    		if np.isnan(temps[i]):
    			temps[i] = temps[i-1]
    	return temps, year, month, day

    def build_temp_calender(self, temps, year, month, day):

        day_of_year = np.zeros(temps.size)
        for i_row in range(temps.size):
            day_of_year[i_row] = find_day_of_year(year[i_row], month[i_row], day[i_row])
        
        median_temp_calender = np.zeros(366)
        for i_day in range(0,365):
            low_day = i_day - 5
            high_day = i_day + 4
            if low_day < 0:
                low_day +=365
            if high_day >365:
                high_day += -365
            if low_day < high_day:
                i_window_days = np.where(np.logical_and(day_of_year >= low_day, day_of_year<=high_day))
            else:
                i_window_days = np.where(np.logical_or(day_of_year>=low_day, day_of_year<=high_day))

            ten_day_median = np.median(temps[i_window_days])
            median_temp_calender[i_day] = ten_day_median

            if i_day == 364:
                median_temp_calender[365] = ten_day_median

        return median_temp_calender

    def find_seasonal_temp(self, year, month, day):
        temp_day = find_day_of_year(year, month, day)
        seasonal_temp = self.temp_calender[temp_day]
        return seasonal_temp

    def get_three_day_coefficients(self, residuals):
        slope, intercept = np.polyfit(residuals[:-3], residuals[3:], 1)
        return (slope, intercept)

    def deseasonalize(self, past_temp, temp_day_past):
        deseasonized_temp = past_temp - self.temp_calender[temp_day_past]
        return deseasonized_temp

    def predict_deseasonalized(self, three_day_temp):
        return self.intercept + self.slope * three_day_temp

    def reseasonalize(self, deseasonalized_temp, past_temp):
        return deseasonalized_temp + self.temp_calender[past_temp]

    def predict(self, year, month, day, past_temp):
        temp_day = find_day_of_year(year, month, day)
        temp_day_past = temp_day - 3
        if temp_day_past < 0:
            temp_day_past += 365

        deseasonalized_temps = self.deseasonalize(past_temp, temp_day_past)
        deseasonalized_prediction = self.predict_deseasonalized(deseasonalized_temps)
        prediction = self.reseasonalize(deseasonalized_prediction, past_temp)

        return prediction

def find_day_of_year(year, month, day):
    days_per_month = np.array([31,28,31,30,31,30,31,31,30,31,30,31])
    if year %4 ==0:
        days_per_month[1] += 1
    day_of_year = np.sum(np.array(days_per_month[:month-1])) + day -1 
    return day_of_year


	




