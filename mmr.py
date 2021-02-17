import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import datetime
import time

# match_input = input(
#     'How many previous matches would you like to see? enter 0 for maximum  ')

account_id = '40641415' #Enter account ID here
limit = 1000
queries = {'limit': limit, 'lobby_type': 7}  # lobby type 7 = ranked
current_mmr = 4150

res = requests.get(
    f'https://api.opendota.com/api/players/{account_id}/Matches', params=queries)
data = res.json()


def check_wins(data, current_mmr):
    count = 1
    match_results = [current_mmr]
    match_times = [datetime.date.today()]

    for matches in data:
        match_id = matches['match_id']
        request_url = f'https://api.opendota.com/api/matches/{match_id}'
        print(f'Fetching match {count}/{limit} ({request_url})', end =" ")
        count += 1

        match_res = requests.get(request_url)
        while match_res.status_code != 200:
            wait_time = 30
            print(str(match_res.status_code) + f" Retrying after {wait_time} seconds...", end = " ")
            time.sleep(wait_time)
            match_res = requests.get(request_url)
        
        print(match_res.status_code)

        start_time = match_res.json()['start_time']
        start_time = datetime.datetime.fromtimestamp(start_time).date()

        # start_time = mdate.epoch2num(start_time)
        mmr_status = False

        if matches['radiant_win'] == True and matches['player_slot'] <= 127:
            mmr_status = True
        elif matches['radiant_win'] == False and matches['player_slot'] > 127:
            mmr_status = True
        
        is_solo_queue = (matches['party_size'] == 1)

        if is_solo_queue and mmr_status:
            current_mmr = current_mmr - 30
        elif is_solo_queue and not mmr_status:
            current_mmr = current_mmr + 30
        elif not is_solo_queue and mmr_status:
            current_mmr = current_mmr - 20
        elif not is_solo_queue and not mmr_status:
            current_mmr = current_mmr + 20
    
        if not match_results:
            match_results.append(current_mmr)
            match_times.append(start_time)
        else:
            if match_times[-1] != start_time:
                # match_results[-1] = current_mmr
            # else:
                match_results.append(current_mmr)
                match_times.append(start_time)

    # reverses list to set origin from furthest back requested match
    match_results.reverse()
    match_times.reverse()
    return match_results, match_times


match_results, match_times = check_wins(data, current_mmr)


print(match_results)
print(match_times)

fig, ax = plt.subplots()

match_times = mdate.date2num(match_times)
# Plot the date using plot_date rather than plot
ax.plot_date(match_times, match_results, ".-")

# for i in range(len(match_results)):
#     if i%10 == 0:
#         ax.annotate(match_results[i], (match_times[i], match_results[i]))

# Choose your xtick format string
date_fmt = '%b-%d-%Y'

# Use a DateFormatter to set the data to the correct format.
date_formatter = mdate.DateFormatter(date_fmt)
ax.xaxis.set_major_formatter(date_formatter)

# Sets the tick labels diagonal so they fit easier.
fig.autofmt_xdate()

plt.show()