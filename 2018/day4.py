import sys
from collections import defaultdict


FALL_ASLEEP = 0
WAKE_UP = 1
BEGIN_SHIFT = 2


ASLEEP = 0
AWAKE = 1


def parse_log_line(line):
    tokens = line.split()
    date = tokens[0][1:]
    time = [int(w) for w in tokens[1][:-1].split(':')]
    log_action = ' '.join(tokens[2:])
    if log_action == 'falls asleep':
        return (date, time, 0, FALL_ASLEEP)
    elif log_action == 'wakes up':
        return (date, time, 0, WAKE_UP)
    else:
        guard = int(tokens[3][1:])
        return (date, time, guard, BEGIN_SHIFT)


def main():
    lines = sorted(line.strip() for line in sys.stdin.readlines())
    logs = [parse_log_line(line) for line in lines]

    active_guard, status, sleep_time = 0, AWAKE, 0
    guard_sleep_times = defaultdict(int)
    guard_sleep_minutes = defaultdict(int)

    for (date, time, guard, action) in logs:
        if action == BEGIN_SHIFT:
            # update outgoing guard's sleeping time
            if status == ASLEEP:
                for minute in range(sleep_time, time[1]):
                    guard_sleep_minutes[(guard, minute)] += 1
                guard_sleep_times[guard] += time[1] - sleep_time

            active_guard = guard
            status = AWAKE
        elif action == FALL_ASLEEP:
            status = ASLEEP
            sleep_time = time[1]
        else:
            if status == ASLEEP:
                for minute in range(sleep_time, time[1]):
                    guard_sleep_minutes[(active_guard, minute)] += 1
                guard_sleep_times[active_guard] += time[1] - sleep_time
            
            status = AWAKE
    
    _, worst_guard = max((time, guard) for (guard, time) in guard_sleep_times.items())

    worst_guard_sleep_by_minute = defaultdict(int)
    for (guard, minute), sleep_count in guard_sleep_minutes.items():
        if guard == worst_guard:
            worst_guard_sleep_by_minute[minute] += sleep_count
    
    _, worst_guard2, worst_minute2 = max((sleep_count, guard, minute) for (guard, minute), sleep_count in guard_sleep_minutes.items())

    _, worst_minute = max((total, minute) for minute, total in worst_guard_sleep_by_minute.items())
    print(worst_guard * worst_minute)
    print(worst_guard2 * worst_minute2)


if __name__ == '__main__':
    main()