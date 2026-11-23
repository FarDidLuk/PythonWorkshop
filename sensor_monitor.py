import os
import random
import csv
import numpy as np
import matplotlib.pyplot as plt


# 1. Get user input

def get_user_input():

    print("\n SENSOR MONITOR")

    sensor_type = input("Enter sensor type (Temperature/Light): ").strip()

    while not sensor_type:
        print("Please enter a sensor type.")
        sensor_type = input("Enter sensor type: ").strip()

    while True:
        try:
            count = int(input("Enter number of readings: "))

            if count <= 0:
                print("Number of readings must be positive.")
                continue

            break

        except ValueError:
            print("Please enter a valid whole number.")

    while True:
        try:
            minimum = float(input("Enter minimum sensor value: "))
            maximum = float(input("Enter maximum sensor value: "))

            if minimum >= maximum:
                print("Minimum must be less than maximum.")
                continue

            break

        except ValueError:
            print("Please enter valid numbers.")

    while True:
        try:
            threshold = float(input("Enter alert threshold: "))
            break

        except ValueError:
            print("Please enter a valid number.")

    return sensor_type, count, minimum, maximum, threshold


# 2. Generate sensor readings

def generate_readings(count, minimum, maximum):

    random.seed(42)

    readings = []

    for _ in range(count):

        value = round(random.uniform(minimum, maximum), 2)

        readings.append(value)

    return readings


# 3. Calculate statistics with NumPy

def calculate_statistics(readings):

    mean = np.mean(readings)

    minimum = np.min(readings)

    maximum = np.max(readings)

    standard_deviation = np.std(readings)

    number_of_readings = len(readings)

    return (mean, minimum, maximum,
            standard_deviation, number_of_readings)


# 4. Find readings above the alert threshold

def find_outliers(readings, threshold):

    alert_readings = [
        reading for reading in readings
        if reading > threshold
    ]

    return alert_readings


# Display the analysis

def display_statistics(readings, threshold):

    mean, minimum, maximum, standard_deviation, number_of_readings = calculate_statistics(
        readings)

    alert_readings = find_outliers(readings, threshold)

    print("\n===== SENSOR DATA ANALYSIS =====")

    print("Number of readings:", number_of_readings)

    print("Mean:", round(mean, 2))

    print("Minimum:", minimum)

    print("Maximum:", maximum)

    print("Standard deviation:", round(standard_deviation, 2))

    print("Alert threshold:", threshold)

    print("Number of readings above threshold:", len(alert_readings))

    print("Readings above threshold:", alert_readings)


# 5. Save readings to CSV

def save_readings(readings, filename="sensor_readings.csv"):

    try:

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), filename), "w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow(["Sample Number", "Sensor Reading"])

            for number, reading in enumerate(readings, start=1):

                writer.writerow([number, reading])

        print("\nData successfully saved to", filename)

        return True

    except (OSError, csv.Error) as error:

        print("Error saving CSV file:", error)

        return False


# 6. Load readings from an existing CSV file

def load_readings(filename):

    sample_numbers = []
    readings = []

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), filename), "r", newline="") as file:

        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("CSV file is empty.")

        required_columns = ["Sample Number", "Sensor Reading"]

        if not all(column in reader.fieldnames for column in required_columns):
            raise ValueError(
                "CSV must contain Sample Number and Sensor Reading columns.")

        for row in reader:

            sample_number = int(row["Sample Number"])
            reading = float(row["Sensor Reading"])

            sample_numbers.append(sample_number)
            readings.append(reading)

    if not readings:
        raise ValueError("CSV file contains no sensor readings.")

    return sample_numbers, readings


# 7. Visualize sensor readings with a line plot

def plot_readings(readings, threshold, sensor_type, sample_numbers=None):

    if sample_numbers is None:
        sample_numbers = range(1, len(readings) + 1)

    plt.figure(figsize=(10, 6))

    plt.plot(
        sample_numbers,
        readings,
        marker="o",
        linestyle="-",
        color="blue",
        label="Sensor Readings"
    )

    plt.axhline(
        y=threshold,
        color="red",
        linestyle="--",
        label="Alert Threshold"
    )

    plt.title(sensor_type + " Sensor Readings")

    plt.xlabel("Sample Number")

    plt.ylabel("Sensor Value")

    plt.grid(True)

    plt.legend()

    plt.tight_layout()

    plt.show()


# 8. Create a histogram

def plot_histogram(readings, sensor_type):

    plt.figure(figsize=(10, 6))

    plt.hist(
        readings,
        bins=10,
        color="blue",
        edgecolor="black"
    )

    plt.title(sensor_type + " Sensor Reading Distribution")

    plt.xlabel("Sensor Value")

    plt.ylabel("Frequency")

    plt.grid(True)

    plt.tight_layout()

    plt.show()


# 9. Main function

def main():

    print("\n SENSOR DATA ANALYSIS ")

    print("1. Generate new sensor readings")

    print("2. Load existing CSV data")

    while True:

        choice = input("\nChoose option (1 or 2): ")

        if choice in ["1", "2"]:
            break

        print("Invalid choice. Please enter 1 or 2.")

    if choice == "1":

        sensor_type, count, minimum, maximum, threshold = get_user_input()

        readings = generate_readings(count, minimum, maximum)

        sample_numbers = None

        save_readings(readings)

    else:

        sensor_type = input("Enter sensor type: ").strip()

        while not sensor_type:
            print("Please enter a sensor type.")
            sensor_type = input("Enter sensor type: ").strip()

        filename = input("Enter CSV filename: ").strip()

        if not filename:
            filename = "sensor_readings.csv"

        try:

            sample_numbers, readings = load_readings(filename)

        except (OSError, ValueError, csv.Error) as error:

            print("Error loading CSV file:", error)

            return

        while True:

            try:
                threshold = float(input("Enter alert threshold: "))
                break

            except ValueError:
                print("Please enter a valid number.")

    # Analyze the sensor readings

    display_statistics(readings, threshold)

    # Display both graphs

    plot_readings(readings, threshold, sensor_type, sample_numbers)

    plot_histogram(readings, sensor_type)


# Start the program

if __name__ == "__main__":
    main()
