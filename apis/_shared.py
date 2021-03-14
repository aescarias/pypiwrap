def convert_bytes_to_readable(num, iec_units=False):
    metric_suffixes = ["B", "KB", "MB", "GB", "TB"]
    iec_suffixes = ["B", "KiB", "MiB", "GiB", "TiB"]
    suffixes = []
    step_unit = 0
    if iec_units:
        suffixes = [*iec_suffixes]
        step_unit = 1024
    else:
        suffixes = [*metric_suffixes]
        step_unit = 1000
    
    for suffix in suffixes:
        if num < step_unit:
            return f"{num:.2f} {suffix}"
        num /= step_unit