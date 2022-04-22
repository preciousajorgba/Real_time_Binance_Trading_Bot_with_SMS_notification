

# Simple Moving Average
def sma(src, length):
    if len(src) < length:
        return None
    return sum(src[-length:]) / float(length)

#   Exponential
EMA = []
def ema(src, length, reset = False):
    global EMA
    if reset: EMA = []; return  
    if len(src) < length: return  
    alpha = 2 / (length + 1)  
    if len(EMA) == 0:
        EMA.append(sma(src, length))
    else:
        EMA.append(alpha * src[-1] + (1 - alpha) * EMA[-1])
    return EMA
