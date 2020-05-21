from datetime import datetime, timedelta

def t_range(*args, step=None):
    """A datetime generator function

    Parameters:
    *args - [start, [end]]
      only accepts datetime.datetime
      defaults:
        start: now (utc)
        end: start + step * 10

    step - increment size or number of steps
      accepts datetime.timedelta or int
      if step is an int type, it is converted to a timedelta:
        step_timedelta = (end - start) / step_int
      defaults:
        with start in *args:
          step = 1 hour
        with start+end in *args:
          step = (end - start) / 10
    """
    assert all([isinstance(arg, datetime) for arg in args]), \
        'Expected datetime.datetime for start, [end]'
    if step:
        assert isinstance(step, (timedelta, int)), 'Expected timedelta or int for step'
    def loop(start, end, step):
        t = start
        while t < end:
            yield t
            t += step
    if len(args) == 0:
        start = datetime.utcnow()
        for t in t_range(start, step=step):
            yield t
    elif len(args) == 1:
        start = t = args[0]
        if not step:
            step = timedelta(hours=1)
        if isinstance(step, timedelta):
            end = start + step * 10
        else:
            end = start + timedelta(hours=step)
            step = (end - start) / step
        for t in loop(start, end, step):
            yield t
    elif len(args) == 2:
        start, end = args
        if not step:
            step = (end - start) / 10
        elif isinstance(step, int):
            step = (end - start) / step
        t = start
        for t in loop(start, end, step):
            yield t
    else:
        raise TypeError(f't_range expected at most 2 arguments, got {len(args)}')
