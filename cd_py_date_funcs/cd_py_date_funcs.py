import math

from cd_py_consts import JD2000, SEC_IN_1_DAY


def gregorian_date_to_sec_from_j2000(year, month, day, hour, minutes, seconds):
    """
    int year, int month, int day, int hour, int minutes, int seconds


    https://ru.wikipedia.org/wiki/%D0%AE%D0%BB%D0%B8%D0%B0%D0%BD%D1%81%D0%BA%D0%B0%D1%8F_%D0%B4%D0%B0%D1%82%D0%B0
    """
    JD2000 = 2451545.0  # 12:00 UT on January 1, 2000

    """
    You must compute first the number of years (y) and months (m) 
    since March 1 -4800 (March 1, 4801 BC)

    """
    a = math.floor((14 - month) / 12)
    # print("a={}\n".format(a))
    y = year + 4800 - a
    # print("y={}\n".format(y))
    m = month + 12 * a - 3
    # print("m={}\n".format(m))

    """
    //All years in the BC era must be converted to astronomical years, 
    //so that 1 BC is year 0, 2 BC is year −1, etc. Convert to a negative number, then increment toward zero.
    //JDN — это номер юлианского дня (англ. Julian Day Number), 
    //который начинается в полдень числа, для которого производятся вычисления.
    //Then, if starting from a Gregorian calendar date compute:
    """
    jdn = (
        day
        + math.floor((153 * m + 2) / 5)
        + 365 * y
        + math.floor(y / 4)
        - math.floor(y / 100)
        + math.floor(y / 400)
        - 32045
    )

    # temp_jdn = jdn
    # temp_hour = hour

    # теперь отталкиваясь от полдня корректируемся на часы минуты и секунды
    if hour < 12:
        jdn -= 0.5
    else:
        hour -= 12

    jdn += (hour * 60 * 60 + minutes * 60 + seconds) / 86400.0
    # print("\nJulian Day = {}".format(jdn))

    date_in_sec = (jdn - JD2000) * 86400
    # print("date in seconds = {}\n".format(date_in_sec))

    # date_in_sec1 = (temp_jdn - JD2000) * 86400
    # if temp_hour < 12:
    #    date_in_sec1 -= 43200
    # date_in_sec1 += temp_hour * 60 * 60 + minutes * 60 + seconds
    # print("date in seconds1 = {}\n".format(date_in_sec1))
    # print("\n")

    return date_in_sec


def gregorian_date_to_jd(year, month, day, hour, minutes, seconds):
    """
    int year, int month, int day, int hour, int minutes, int seconds


    https://ru.wikipedia.org/wiki/%D0%AE%D0%BB%D0%B8%D0%B0%D0%BD%D1%81%D0%BA%D0%B0%D1%8F_%D0%B4%D0%B0%D1%82%D0%B0


    https://astronomy.stackexchange.com/questions/49790/calculation-of-julian-day-is-off-for-negative-dates/49799#49799

    """

    """
    You must compute first the number of years (y) and months (m) 
    since March 1 -4800 (March 1, 4801 BC)

    """
    a = math.floor((14 - month) / 12)
    # print("a={}\n".format(a))
    y = year + 4800 - a
    # print("y={}\n".format(y))
    m = month + 12 * a - 3
    # print("m={}\n".format(m))

    """
    //All years in the BC era must be converted to astronomical years, 
    //so that 1 BC is year 0, 2 BC is year −1, etc. Convert to a negative number, then increment toward zero.
    //JDN — это номер юлианского дня (англ. Julian Day Number), 
    //который начинается в полдень числа, для которого производятся вычисления.
    //Then, if starting from a Gregorian calendar date compute:
    """
    jdn = (
        day
        + math.floor((153 * m + 2) / 5)
        + 365 * y
        + math.floor(y / 4)
        - math.floor(y / 100)
        + math.floor(y / 400)
        - 32045
    )

    # temp_jdn = jdn
    # temp_hour = hour

    # теперь отталкиваясь от полдня корректируемся на часы минуты и секунды
    if hour < 12:
        jdn -= 0.5
    else:
        hour -= 12

    jdn += (hour * 60 * 60 + minutes * 60 + seconds) / 86400.0
    # print("\nJulian Day = {}".format(jdn))

    return jdn


# used in find_eps formula
# https://radixpro.com/a4a-start/factor-t-and-delta-t/
# https://radixpro.com/a4a-start/obliquity/
def factor_t(sec_from_jd2000):
    jdn = JD2000 + sec_from_jd2000 / SEC_IN_1_DAY
    return (jdn - JD2000) / 36525


# отличная версия калькуляции, получаем Грег. дату в ET
def sec_jd2000_to_greg_meeus(sec_from_jd2000):
    # получаем Julian Day
    jdn = JD2000 + sec_from_jd2000 / SEC_IN_1_DAY

    jdn += 0.5

    A = None

    Z = math.trunc(jdn)

    F = jdn - Z

    if Z < 2299161:
        A = Z
    else:
        alpha = math.trunc((Z - 1867216.25) / 36524.25)
        A = Z + 1 + alpha - math.trunc(alpha / 4)

    B = A + 1524

    C = math.trunc((B - 122.1) / 365.25)

    D = math.trunc(365.25 * C)

    E = math.trunc((B - D) / 30.6001)

    day = B - D - math.trunc(30.6001 * E) + F

    month = None

    if E < 0 or E > 15:
        print("sec_jd2000_to_greg_meeus, unacceptable value of E")
        raise ValueError

    if E < 14:
        month = E - 1
    else:
        month = E - 13

    year = C - 4716 if month > 2 else C - 4715

    hour = (day - math.trunc(day)) * 24

    day = math.trunc(day)

    minute = (hour - math.trunc(hour)) * 60

    hour = math.trunc(hour)

    second = (minute - math.trunc(minute)) * 60

    minute = math.trunc(minute)

    second = math.ceil(second)

    return year, month, day, hour, minute, second


def greg_date_to_JD_fliegel(year, month, day, hour, minutes, seconds):
    return (
        367 * year
        - (7 * (year + 5001 + (month - 9) / 7)) / 4
        + (275 * month) / 9
        + day
        + 1729777
        + (hour + minutes / 60 + seconds / 3600) / 24
    )


def JD_to_greg_fliegel(JD):
    """
    Convert Julian Day to Gregorian date using Fliegel-Van Flandern algorithm.
    """
    JD = JD + 0.5
    Z = math.trunc(JD)
    F = JD - Z
    A = Z
    if Z >= 2299161:
        alpha = math.trunc((Z - 1867216.25) / 36524.25)
        A = Z + 1 + alpha - math.trunc(alpha / 4)
    B = A + 1524
    C = math.trunc((B - 122.1) / 365.25)
    D = math.trunc(365.25 * C)
    E = math.trunc((B - D) / 30.6001)
    day = B - D - math.trunc(30.6001 * E) + F
    month = E - 1 if E < 14 else E - 13
    year = C - 4716 if month > 2 else C - 4715
    hour = (day - math.trunc(day)) * 24
    day = math.trunc(day)
    minute = (hour - math.trunc(hour)) * 60
    hour = math.trunc(hour)
    second = (minute - math.trunc(minute)) * 60
    minute = math.trunc(minute)
    second = math.ceil(second)
    return year, month, day, hour, minute, second


def gregorian_to_julian_day(year, month, day):
    """
    Convert a Gregorian date to Julian Day using the Fliegel algorithm.
    """
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3

    # Calculate Julian Day
    julian_day = (
        day + ((153 * m + 2) // 5) + 365 * y + y // 4 - y // 100 + y // 400 - 32045
    )

    return julian_day


def gregorian_date_to_julian_day_with_time(year, month, day, hour, minutes, seconds):
    """
    Convert a Gregorian date to Julian Day with time using the Fliegel algorithm.
    """
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3

    # Calculate Julian Day
    julian_day = (
        day + ((153 * m + 2) // 5) + 365 * y + y // 4 - y // 100 + y // 400 - 32045
    )

    # Add time
    julian_day += (hour + minutes / 60 + seconds / 3600) / 24

    return julian_day


def gregorian_to_JD_gpt(year, month, day):
    """
        Convert a Gregorian calendar date to Julian Day.

        :param year: Year
        :param month: Month
        :param day: Day
        :return: Julian Day





    JD=⌊365.25×(year+4716)⌋+⌊30.6001×(month+1)⌋+day+B−1524.5

    Where B is a correction term to account for the change from Julian to Gregorian calendar.

    This algorithm works well for dates after 1582, when the Gregorian calendar was adopted.
    For dates before 1582, you may need to adjust the algorithm to account for the transition from the Julian to the Gregorian calendar.
    """
    if month <= 2:
        year -= 1
        month += 12

    A = year // 100
    B = 2 - A + (A // 4)

    jd = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + B - 1524.5

    return jd


def greg_to_JD_with_time(year, month, day, hour, minute, second):
    """
    Convert a Gregorian calendar date and time to Julian Day.

    :param year: Year
    :param month: Month
    :param day: Day
    :param hour: Hour
    :param minute: Minute
    :param second: Second
    :return: Julian Day
    """
    if month <= 2:
        year -= 1
        month += 12

    A = year // 100
    B = 2 - A + (A // 4)

    jd = (
        (int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + B - 1524.5)
        + (hour - 12) / 24
        + minute / 1440
        + second / 86400
    )

    return jd


"""	
// delta_t observations started at 1620 and now it is 2017
// so we have 398 records for now
// each record is the year and a number of seconds
// [0] record corresponds to year 1620
// https://www.staff.science.uu.nl/~gent0113/deltat/deltat.htm
// ftp://maia.usno.navy.mil/ser7/deltat.data

/*
http://astro.ukho.gov.uk/nao/miscellanea/DeltaT/
https://ru.wikipedia.org/wiki/%D0%94%D0%B5%D0%BB%D1%8C%D1%82%D0%B0_T
https://eclipse.gsfc.nasa.gov/SEhelp/deltatpoly2004.html
https://en.wikipedia.org/wiki/%CE%94T

struct delta_t_table_struct{
    int year;
    double seconds;
};
"""

full_delta_t_table = [
    [1950, 29.15],
    [1951, 29.57],
    [1952, 29.97],
    [1953, 30.36],
    [1954, 30.72],
    [1955, 31.07],
    [1956, 31.35],
    [1957, 31.68],
    [1958, 32.18],
    [1959, 32.68],
    [1960, 33.15],
    [1961, 33.59],
    [1962, 34.0],
    [1963, 34.47],
    [1964, 35.03],
    [1965, 35.73],
    [1966, 36.54],
    [1967, 37.43],
    [1968, 38.29],
    [1969, 39.2],
    [1970, 40.18],
    [1971, 41.17],
    [1972, 42.23],
    [1973, 43.37],
    [1974, 44.49],
    [1975, 45.48],
    [1976, 46.46],
    [1977, 47.52],
    [1978, 48.53],
    [1979, 49.59],
    [1980, 50.54],
    [1981, 51.38],
    [1982, 52.17],
    [1983, 52.96],
    [1984, 53.79],
    [1985, 54.34],
    [1986, 54.87],
    [1987, 55.32],
    [1988, 55.82],
    [1989, 56.3],
    [1990, 56.86],
    [1991, 57.57],
    [1992, 58.31],
    [1993, 59.12],
    [1994, 59.99],
    [1995, 60.78],
    [1996, 61.63],
    [1997, 62.3],
    [1998, 62.97],
    [1999, 63.47],
    [2000, 63.83],
    [2001, 64.09],
    [2002, 64.3],
    [2003, 64.47],
    [2004, 64.57],
    [2005, 64.69],
    [2006, 64.85],
    [2007, 65.15],
    [2008, 65.46],
    [2009, 65.78],
    [2010, 66.07],
    [2011, 66.32],
    [2012, 66.6],
    [2013, 66.91],
    [2014, 67.28],
    [2015, 67.64],
    [2016, 68.1],
    [2017, 69.18],
    [2018, 69.18],
    [2019, 69.18],
    [2020, 69.18],
    [2021, 69.18],
    [2022, 69.18],
    [2023, 69.2],
    [2024, 69.18],
]


"""	
//https://eclipse.gsfc.nasa.gov/SEhelp/deltaT.html
//This parameter is known as delta-T or ΔT (ΔT = TDT - UT).
// for delta_t calculations we use
// https://eclipse.gsfc.nasa.gov/SEcat5/deltatpoly.html
// algorithms
"""


def calculate_delta_t(year):
    delta_t_sec = None

    # before year 1620 (observations started from 1620, before were only estimations)
    if year < 1620:
        if year < -500:
            delta_t_sec = -20 + 32 * math.pow((year - 1820) / 100, 2)
            return delta_t_sec
        elif year >= -500 and year <= 500:
            delta_t_sec = (
                10583.6
                - (1014.41 * year) / 100
                + 33.78311 * math.pow(year / 100, 2)
                - 5.952053 * math.pow(year / 100, 3)
                - 0.1798452 * math.pow(year / 100, 4)
                + 0.022174192 * math.pow(year / 100, 5)
                + 0.0090316521 * math.pow(year / 100, 6)
            )
            return delta_t_sec
        elif year > 500 and year <= 1600:
            delta_t_sec = (
                1574.2
                - (556.01 * (year - 1000)) / 100
                + 71.23472 * math.pow((year - 1000) / 100, 2)
                + 0.319781 * math.pow((year - 1000) / 100, 3)
                - 0.8503463 * math.pow((year - 1000) / 100, 4)
                - 0.005050998 * math.pow((year - 1000) / 100, 5)
                + 0.0083572073 * math.pow((year - 1000) / 100, 6)
            )
            return delta_t_sec
        else:
            # from 1600 to 1620
            delta_t_sec = (
                120
                - 0.9808 * (year - 1600)
                - 0.01532 * math.pow(year - 1600, 2)
                + math.pow(year - 1600, 3) / 7129
            )
            return delta_t_sec

    if year >= 1620 and year <= 1700:
        delta_t_sec = (
            120
            - 0.9808 * (year - 1600)
            - 0.01532 * math.pow(year - 1600, 2)
            + math.pow(year - 1600, 3) / 7129
        )
        return delta_t_sec

    if year > 1700 and year <= 1800:
        delta_t_sec = (
            8.83
            + 0.1603 * (year - 1700)
            - 0.0059285 * math.pow(year - 1700, 2)
            + 0.00013336 * math.pow(year - 1700, 3)
            - math.pow(year - 1700, 4) / 1174000
        )
        return delta_t_sec

    if year > 1800 and year <= 1860:
        delta_t_sec = (
            13.72
            - 0.332447 * (year - 1800)
            + 0.0068612 * math.pow(year - 1800, 2)
            + 0.0041116 * math.pow(year - 1800, 3)
            - 0.00037436 * math.pow(year - 1800, 4)
            + 0.0000121272 * math.pow(year - 1800, 5)
            - 0.0000001699 * math.pow(year - 1800, 6)
            + 0.000000000875 * math.pow(year - 1800, 7)
        )
        return delta_t_sec

    if year > 1860 and year <= 1900:
        delta_t_sec = (
            7.62
            + 0.5737 * (year - 1860)
            - 0.251754 * math.pow(year - 1860, 2)
            + 0.01680668 * math.pow(year - 1860, 3)
            - 0.0004473624 * math.pow(year - 1860, 4)
            + math.pow(year - 1860, 5) / 233174
        )
        return delta_t_sec

    if year > 1900 and year <= 1920:
        delta_t_sec = (
            -2.79
            + 1.494119 * (year - 1900)
            - 0.0598939 * math.pow(year - 1900, 2)
            + 0.0061966 * math.pow(year - 1900, 3)
            - 0.000197 * math.pow(year - 1900, 4)
        )
        return delta_t_sec

    if year > 1920 and year <= 1941:
        delta_t_sec = (
            21.2
            + 0.84493 * (year - 1920)
            - 0.0761 * math.pow(year - 1920, 2)
            + 0.0020936 * math.pow(year - 1920, 3)
        )
        return delta_t_sec

    if year > 1941 and year <= 1961:
        delta_t_sec = (
            29.07
            + 0.407 * (year - 1950)
            - math.pow(year - 1950, 2) / 233.0
            + math.pow(year - 1950, 3) / 2547.0
        )
        return delta_t_sec

    if year > 1961 and year <= 1986:
        delta_t_sec = (
            45.45
            + 1.067 * (year - 1975)
            - math.pow(year - 1975, 2) / 260.0
            - math.pow(year - 1975, 3) / 718.0
        )
        return delta_t_sec

    if year > 1986 and year <= 2005:
        delta_t_sec = (
            63.86
            + 0.3345 * (year - 2000)
            - 0.060374 * math.pow(year - 2000, 2)
            + 0.0017275 * math.pow(year - 2000, 3)
            + 0.000651814 * math.pow(year - 2000, 4)
            + 0.00002373599 * math.pow(year - 2000, 5)
        )
        return delta_t_sec

    if year > 2005 and year <= 2050:
        delta_t_sec = (
            62.92 + 0.32217 * (year - 2000) + 0.005589 * math.pow(year - 2000, 2)
        )
        return delta_t_sec

    if year > 2050 and year <= 2150:
        delta_t_sec = (
            -20 + 32 * math.pow((year - 1820) / 100.0, 2) - 0.5628 * (2150 - year)
        )
        return delta_t_sec

    if year > 2150:
        delta_t_sec = -20 + 32 * math.pow((year - 1820) / 100.0, 2)
        return delta_t_sec

    return -1


def get_delta_t(year):
    first_year = full_delta_t_table[0][0]
    last_year = full_delta_t_table[-1][0]
    if year < first_year or year > last_year:
        return calculate_delta_t(year)

    return full_delta_t_table[year - first_year][1]


"""	
// converts date to timestamp
// https://www.unixtimestamp.com/
// https://stackoverflow.com/questions/9873197/convert-date-to-timestamp-in-javascript
//https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/UTC
// input format - {input_year, input_month, input_day, input_hour, input_minutes, input_seconds}
function date_to_timestamp(date) {
  return (
    new Date(
      Date.UTC(
        date.input_year,
        date.input_month - 1,
        date.input_day,
        date.input_hour,
        date.input_minutes,
        date.input_seconds
      )
    ).getTime() / 1000
  );
}

// Принимает JED и перводит его в sec_from_jd2000
function jed_to_sec_from_jd2000(date) {
  return (date - JD2000) * SEC_IN_1_DAY;
}
"""


if __name__ == "__main__":
    #    print(sec_jd2000_to_greg_meeus(-682470714.47))  # 1978, 5, 17, 12, 47, 17
    #    print(sec_jd2000_to_greg_meeus(-690188753.3732915))
    #    print(sec_jd2000_to_greg_meeus(86400 * 365))
    #    print(sec_jd2000_to_greg_meeus(86400 * 365 * 2))
    #    print(sec_jd2000_to_greg_meeus(86400 * 365 * 3))
    #    print(sec_jd2000_to_greg_meeus(86400 * 365 * 4))

    #    print(gregorian_date_to_sec_from_j2000(1978, 5, 17, 12, 47, 17))
    jd = greg_date_to_JD_fliegel(1978, 5, 17, 12, 47, 17)  # 2443646.032836
    print(jd)

    # Example usage
    year = 1978
    month = 5
    day = 17

    julian_day = gregorian_date_to_julian_day_with_time(year, month, day, 12, 47, 17)
    print(f"The Julian Day for {year}-{month}-{day} is {julian_day}")

    # Example usage
    year = 2024
    month = 2
    day = 25
    hour = 15
    minute = 30
    second = 45

    jd = greg_to_JD_with_time(1978, 5, 17, 12, 47, 17)
    print("Julian Day:", jd)

    jd = gregorian_date_to_jd(1978, 5, 17, 12, 47, 17)
    print(f" Julian Day = {jd}")

    jd = gregorian_date_to_sec_from_j2000(1978, 5, 17, 12, 47, 17)
    print(f" Seconds = {jd}")
    jd = sec_jd2000_to_greg_meeus(jd)
    print(f" Gregorian date = {jd}")
    print(get_delta_t(1800))
    print(get_delta_t(1978))
    print(get_delta_t(2024))
