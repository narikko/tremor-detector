from features import get_absval, get_mean

def filter(data):
    data_abs = get_absval(data)
    mean = get_mean(data_abs)
    filtered_data = []
    
    for i in data:
        if (i < mean * 1.25 and i > mean * -1.25):
            filtered_data.append(i)
    
    return filtered_data
            


