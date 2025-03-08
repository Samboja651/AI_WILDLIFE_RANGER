"""app functions"""
import urllib.error
import urllib.request

def fetch_gps_collar_data(url):
    """
    fetches gps collar data of an animal
    returns data_file
    """
    try:
        with urllib.request.urlopen(url) as f:
            data = f.read().decode('utf-8')
        with open('gps_collar_data.csv', 'w', encoding='utf-8') as f:
            f.write(data)
        print("data downloaded successfully")
        return
    except urllib.error.URLError as e:
        print(f"Error! : {e}")
        return

# fetch_gps_collar_data(URL2)

def read_gps_collar_data(file):
    """
    reads gps collar data from file.
    returns data in keys(columns) and list(val(tuples))
    """
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = f.readlines()

        # get the column names
        keys = data[:1][0].strip().split(",")
        values = []
        for val in data[1:]:
            val = val.strip().split(',')
            values.append(tuple(val))
        return keys, values
    
    except FileExistsError as e:
        print(f"Error! {e}")
        return
    except FileNotFoundError as e:
        print(f"Error! {e}")
        return
    except IndexError as e:
        print(f"Error! {e}")
        return

# read_gps_collar_data("Kiboche_last_500_rows_data.csv")


