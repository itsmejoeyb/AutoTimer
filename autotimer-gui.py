import tkinter as tk 
import json
import sys
from subprocess import Popen

subpro = None

gui = tk.Tk()
gui.title('AutoTimer')
gui.geometry('700x450')

top_frame = tk.Frame(gui).pack()
bottom_frame = tk.Frame(gui).pack(side='bottom')

text = tk.Text(top_frame, height=20, width=90, bg='black', fg='white', wrap='word')
text.pack()

def start():
    text.delete(1.0, tk.END)
    text.insert(1.0, 'Running...')
    global subpro 
    subpro = Popen(['python', './autotimer.py'])

def stop():
    print('Stop')
    try:
        subpro.kill()
    except:
        print('nothing to kill')
    text.delete(1.0,tk.END)
    getTimes()

def getTimes():
    try:
        with open('activities.json') as f:
            data = json.load(f)
            for item in data['activities']:
                item_name = f'Name: {item["name"]}'
                entry_times = []
                for entry in item['time_entries']:
                    entry_times.append(f'Start Time: {entry["start_time"]} | End Time: {entry["end_time"]} | Time Spent: {entry["hours"]}:{entry["minutes"]}:{entry["seconds"]}')
                    fixed_entry_times = '\n'.join(entry_times)
                text.insert(1.0, f'{item_name}\n {fixed_entry_times}\n\n')
    except:
        text.insert(1.0, 'No entries yet today.')

def deleteFile():
    try:
        with open('activities.json') as f:
                data = json.load(f)
                for item in data:
                    del item
                    text.delete(1.0, tk.END)
                    text.insert(1.0, 'List has been cleared.')
    except:
        print('nothing to delete')

getTimes()

startButton = tk.Button(bottom_frame, height=2, width=20, text='Start', command=start).pack()
stopButton = tk.Button(bottom_frame, height=2, width=20, text='Stop', command=stop).pack()
deleteButton = tk.Button(bottom_frame, height=2, width=20, text='Delete', command=deleteFile).pack()

gui.mainloop()
