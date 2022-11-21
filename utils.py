

def parse_ping(line):
    split = line.split()
    if split == []:
        return None, None
    elif split[0] in ['---', 'PING']:
        return None, None
    elif split[1] == 'packets':
        sent = int(split[0])
        lost = sent - int(split[3])
        return 'packets', (sent, lost)
    elif split[0] == 'rtt':
        min, avg, max, std = [float(i) for i in split[3].split('/')]
        return 'rtt', (min, avg, max, std)
    return None, None
