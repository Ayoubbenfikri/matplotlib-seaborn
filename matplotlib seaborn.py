import matplotlib.pyplot as plt
import csv

#data
class FlightData:
    def __init__(self, file_path):
        self.flights = []
        with open(file_path) as file:
            reader = csv.DictReader(file) 
            for row in reader:
                row['passengers'] = int(row['passengers'])
                self.flights.append(row) #{'year': '2010', 'month': 'Jan', 'passengers': '415'.....}
                

    def get_unique_years(self):
        years = []
        for row in self.flights:
            if row['year'] not in years:
                years.append(row['year'])

        return years #list

    def get_unique_months(self):
        months = []
        for row in self.flights:
            if row['month'] not in months:
                months.append(row['month'])
        return months #list

    def get_data_by_year_and_month(self):
        heatmap_data = {}
        for row in self.flights:
            month = row['month']
            year = row['year']
            if month not in heatmap_data:
                heatmap_data[month] = {}
            heatmap_data[month][year] = row['passengers']
        return heatmap_data # dic month , {'Jan': {'2010': '415', '2011': '470',...},'Feb': {'2010': '390', '2011': '445'...}....

# data analyse
class FlightAnalysis:
    def __init__(self, data):
        self.data = data

    def show_menu(self):
        print("\nFLIGHTS DATA ANALYSIS")
        print("1. Show Time Series")
        print("2. Show Monthly Data")
        print("3. Compare Years/Months")
        print("4. Exit")

    def show_time_series(self):
        years = self.data.get_unique_years()
        for year in years:
            months = [] #x
            passengers = [] #y
            for row in self.data.flights: #[{'year': '2010', 'month': 'Jan', 'passengers': '415'.....}...]
                if row['year'] == year:
                    months.append(row['month'])
                    passengers.append(row['passengers'])
            plt.plot(months, passengers, label=year)

        plt.title('Passengers by Month (All Years)')
        plt.xlabel('Month')
        plt.ylabel('Passengers')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def show_monthly_data(self):
        heatmap_data = self.data.get_data_by_year_and_month() #dic {'Jan': {'2010': '415', '2011': '470',...},'Feb': {'2010': '390', '2011': '445'...}....
        months = self.data.get_unique_months() #list ['Jan', 'Feb', 'Mar'...]
        years = self.data.get_unique_years() #list  ['2010', '2011'...]

        plt.figure(figsize=(10, 6))
        data = []
        for month in months:
            row_data = []
            for year in years:
                row_data.append(heatmap_data[month].get(year)) #
            data.append(row_data) #[jan_passan[415,470...],fev_passan[390,445]...]
        plt.imshow(data, cmap='Blues') # YlOrRd,Blues, viridis ,coolwarm
        plt.colorbar(label='Passengers')

        for i in range(len(months)):
            for j in range(len(years)):
                value = heatmap_data[months[i]].get(years[j])
                plt.text(j, i, value, ha='center', va='center', color='black', fontsize=8)

        plt.xticks(range(len(years)), years, rotation=45)
        plt.yticks(range(len(months)), months)
        plt.title('Monthly Passengers Heatmap')
        plt.show()

    def compare_years_months(self):
        print("\nCompare Options:")
        print("1. Compare years")
        print("2. Compare months")
        sub_choice = input("Enter your choice (1-2): ")

        if sub_choice == '1':
            years_input = input("Enter years to compare (comma separated): ").split(',')
            data = {}
            for year in years_input:
                year = year.strip()
                total_passengers = 0
                for row in self.data.flights: #[{'year': '2010', 'month': 'Jan', 'passengers': '415'.....},...]
                    if row['year'] == year:
                        total_passengers += int(row['passengers'])
                data[year] = total_passengers # {'year':'total_passangers'.....} 

            plt.bar(data.keys(), data.values(), color=['skyblue'])
            plt.xlabel('Years')
            plt.ylabel('Total Passengers')
            plt.title('Yearly Comparison of Passengers')
            plt.show()


        elif sub_choice == '2':
            months_input = input("Enter months to compare (comma separated): ").split(',')
            data = {}
            for month in months_input:
                month = month.strip().capitalize()
                total_passengers = 0
                for row in self.data.flights:
                    if row['month'] == month:
                        total_passengers += row['passengers']
                data[month] = total_passengers #{'jan':''total_passengers'....}

            plt.bar(data.keys(), data.values(), color='lightgreen')
            plt.xlabel('Months')
            plt.ylabel('Total Passengers')
            plt.title('Monthly Comparison of Passengers')
            plt.tight_layout()
            plt.show()


def main():
    flight_data = FlightData('flights.csv')
    flight_analysis = FlightAnalysis(flight_data)

    while True:
        flight_analysis.show_menu()
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            flight_analysis.show_time_series()
        elif choice == '2':
            flight_analysis.show_monthly_data()
        elif choice == '3':
            flight_analysis.compare_years_months()
        elif choice == '4':
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
