import time


# ignore
def test_get_info():
    info = time.get_clock_info('monotonic')
    print(info)


# ignore
def test_display_formats():
    formats = ["%a ",
               "%A ",
               "%b",
               "%B",
               "%c",
               "%d",
               "%H",
               "%I",
               "%j",
               "%m",
               "%M",
               "%p",
               "%S",
               "%U",
               "%w",
               "%W",
               "%x",
               "%X",
               "%y",
               "%Y",
               "%z",
               "%Z",
               "%%"]

    for f in formats:
        t = time.strftime(f, time.localtime())
        print(f, ':', t)


def get_day_and_time():
    day_and_time = time.strftime("%A %X", time.localtime())
    day_and_time = day_and_time.split(" ")
    return day_and_time


if __name__ == '__main__':
    # test_display_formats()
    print(get_day_and_time())
