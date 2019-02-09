import sys
import predict_weather as pw

def decide(test_year=2015, test_month=7, test_day=25, test_temp=95):
	predictor = pw.Predictor()
	prediction = predictor.predict(test_year, test_month, test_day, test_temp)
	print('predicted temperature is', prediction)
	if prediction >= 90:
		decision = True
	else:
		decision = False

	return decision

if __name__ == '__main__':
	if len(sys.argv)<5:
		print('Input Format')
		print('		python buy_tickets.py <year> <month> <day> <temp>')
	else:
		year = int(sys.argv[1])
		month = int(sys.argv[2])
		day = int(sys.argv[3])
		temp = int(sys.argv[4])
	decision = decide(year, month, day, temp)
	if decision:
		print("But tickets")
	else:
		print("Dont buy")

# python buy_tickets.py 2015 7 25 95