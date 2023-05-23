from datetime import datetime

def to_float(value):
    try:
        return float(value)
    except:
        return 0
    
def get_date_and_location(file):
    next(file, None)
    line = next(file).strip()
    list_line = line.split(",")
    date_list = list_line[0].split(" - ")
    date_info = date_list[0]
    
    # Convert date_info to a datetime object
    date_info_dt = datetime.strptime(date_info, "%m/%d/%y")

    location_list = list_line[-2].split(" - ")
    location_info = location_list[-1]
    return date_info_dt, location_info
