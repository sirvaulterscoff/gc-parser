from string import ascii_letters
import re
real_time_re = re.compile('real=(.*?) secs')
heap = re.compile('Full GC.*?\[.*?\] \[.*?\] (\d+)K->(\d+)K\((\d+)K\)')
def parse(_format, file_name):
    f = file(file_name, 'r')
    _str = f.readline()
    stop_time = 0.0
    app_time = 0.0
    letts = ascii_letters + ':'

    last_gc_time = None
    young_gc = []
    old_gc = []
    full_gc = []
    heap_usg = []
    max_heap = 0
    while (_str):
        if _str.startswith('Application time:'): #measure total app time
            atime = _str.translate(None, letts)
            val = atime.replace(',', '.')
            if val.strip():
                try:
                    app_time += float(val)
                except :
                    pass
            _str = f.readline()
            continue
        if _str.startswith('Total time for which'):
            atime = _str.translate(None, ascii_letters + ':')
            val = atime.replace(',', '.')
            if val.strip():
                try:
                    stop_time += float(val)
                except:
                    pass
            _str = f.readline()
            continue
        #if _str.find('[GC') != -1:
        #    gc_time = float(_str[0: _str.find(':')])
        #if _str.find('[PSYoungGen') != -1 or _str.find('[ParNew') != -1 or _str.find('[DefNew') != -1:
        #    young_gc.append(gc_time)
        #if _str.find('[PSOldGen') != -1 or _str.find('CMS-initial-mark') != -1 or _str.find('[ParOldGen') != -1:
        #    old_gc.append(gc_time)
        if _str.find('[Full GC') != -1:
            gc_time = float(_str[0: _str.find(':')].replace(',', '.'))

            match = real_time_re.search(_str)
            full_gc_time_cur = 0
            if match:
                full_gc_time_cur = float(match.group(1).replace(',','.'))
            match = heap.search(_str)
            if match:
                used = match.group(1)
                after = match.group(2)
                total = match.group(3)
                freed = int(used) - int(after)
                full_gc.append( (gc_time, full_gc_time_cur, int(after), freed, int(total)) )
            else:
                full_gc.append( (gc_time,  full_gc_time_cur, 0 ) )

        _str = f.readline()

    f.close()
    return full_gc

