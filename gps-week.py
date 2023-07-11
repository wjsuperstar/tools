import time

def Utc2GpsWeek(utc_time):
    gps_start = "1980-01-06 00:00:00"
    gps_start_sec = time.mktime(time.strptime(gps_start, "%Y-%m-%d %H:%M:%S"))
    return (utc_time-gps_start_sec)/(86400*7);
    

if __name__ == '__main__':
    gps_week = Utc2GpsWeek(time.time())
    print("gps_week:", gps_week);

