async def sorting_count(arr: list) -> list:
    for i in range(len(arr)):
        for j in range(len(arr) - i - 1):
            if arr[j][0] > arr[j + 1][0]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr


async def convert_time_count(s: str) -> int:
    s = s.split(':')
    minute = int(s[0])
    second = int(s[1])

    count = minute * 60 + second
    return count


async def convert_to_time(s: int) -> str:
    minute = s // 60
    second = s % 60
    if minute < 10:
        minute = '0' + str(minute)
        if second < 10:
            second = '0' + str(second)

            return f'{minute}:{second}'
        else:
            return f'{minute}:{second}'
    else:
        return f'{minute}:{second}'