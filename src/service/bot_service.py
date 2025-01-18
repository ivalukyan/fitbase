async def sorting_count_up(arr: list) -> list:
    for i in range(len(arr)):
        for j in range(len(arr) - i - 1):
            if arr[j][0] > arr[j + 1][0]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr


async def sorting_count_down(arr: list) -> list:
    for i in range(len(arr)):
        for j in range(len(arr) - i - 1):
            if arr[j][0] < arr[j + 1][0]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr


async def convert_time_count(arr: list) -> list:
    for i in range(len(arr)):
        s = arr[i][0].split(':')
        minute = int(s[0])
        second = int(s[1])
        count = minute * 60 + second
        arr[i][0] = count
    return arr


async def convert_to_time(arr: list) -> list:
    for i in range(len(arr)):
        minute = arr[i][0] // 60
        second = arr[i][0] % 60
        if minute < 10:
            minute = '0' + str(minute)
            if second < 10:
                second = '0' + str(second)

                arr[i][0] = f'{minute}:{second}'
            else:
                arr[i][0] = f'{minute}:{second}'
        else:
            arr[i][0] = f'{minute}:{second}'
    return arr


async def row_to_list(arr: list) -> list:
    data = []
    for i in range(len(arr)):
        data.append(list(arr[i]))
    return data