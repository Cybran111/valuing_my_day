import math
from datetime import date
from tkinter import *

class Deal:

    objects = []

    def __init__(self, name, time, effort, discipline=0, desc=''):
        self.name, self.time, self.effort, self.discipline, self.desc = name, time, effort, discipline, desc
        Deal.objects.append(self)

    def get_value(self):
        if self.discipline is 0:
            return math.sqrt(self.time**2+self.effort**2)
        else:
            return (self.time**3+self.effort**3+self.discipline**3)**(1/3)

    def __str__(self):
        return self.name+'\t'+(self.desc+'\t' if self.desc != '' else '')


class Day:

    objects = []

    def __init__(self, date_, deals=dict()):
        self.day_date, self.deals = date_, deals
        Day.objects.append(self)

    def update_deal(self, deal, is_completed=False):
        self.deals[deal.name] = {'completed': is_completed, 'deal': deal}

    def add_deal(self, deal, is_completed=False):
        if not deal.name in self.deals.keys():
            self.update_deal(deal, is_completed)
        else:
            print('you already have deal named', deal.name+'.')

    def remove_deal(self, name):
        if name in self.deals.keys():
            del self.deals[name]

    def complete_by_name(self, name):
        if name in self.deals.keys():
            self.deals[name]['completed'] = True
        else:
            print('there is no deal named "', name, '".', sep='')

    def get_net_value(self):
        v = 0
        for i in self.deals.values():
            v += i['deal'].get_value() if i['completed'] else 0
        v /= len(self.deals.keys())
        return v

    def print_all_deals(self):
        for i in self.deals.keys():
            print(self.deals[i]['deal'], self.deals[i]['completed'], sep='\t')

    def __str__(self):
        return str(self.day_date)


class DayVisualiser:

    def __init__(self, days):
        self.days = days
        self.root = Tk()
        self.root.geometry('+500+300')
        self.root.title('Day Valuer')
        self.root.resizable(False, False)
        # creating 2 toolbars
        self.frm1 = Frame(self.root, width=300, heigh=500)
        self.frm2 = Frame(self.root, width=300, heigh=500)
        self.frm1.pack(side='left')
        self.frm2.pack(side='right')
        # creating profile crud buttons
        self.new_profile_btn = Button(self.root, text='New Profile')
        self.new_profile_btn.pack(side='top')
        self.rm_profile_btn = Button(self.root, text='Remove this Profile')
        self.rm_profile_btn.pack(side='top')
        # graph button
        self.graph_btn = Button(self.root, text='Graph day', command=self.graph_day)
        self.graph_btn.pack(side='top')
        # left toolbar - day list
        self.day_list = Listbox(self.frm1, selectmode=SINGLE)
        for item in self.days:
            self.day_list.insert(END, str(item))
        self.day_list.pack()
        # load day button
        self.load_day_btn = Button(self.frm1, text='Load day', command=self.day_change_react)
        self.load_day_btn.pack(side='bottom', expand=False)
        # show description button
        self.show_day_desc = Button(self.frm1, text='Day info', command=self.show_day_info)
        self.show_day_desc.pack()
        # second list - todo list
        self.task_list = Listbox(self.frm2, selectmode=SINGLE)
        self.task_list.pack()
        # task controls - delete
        self.delete_task_btn = Button(self.frm2, text='Delete task', command=self.delete_task)
        self.delete_task_btn.pack(side='bottom')
        # task controls - show info
        self.show_info_btn = Button(self.frm2, text='Show info', command=self.show_info)
        self.show_info_btn.pack(side='right')
        # task controls - toggle task checked
        self.check_task_btn = Button(self.frm2, text='Check deal', command=self.check_deal)
        self.check_task_btn.pack(side='left')

        self.sel_day = self.days[0]
        self.sel_deal = self.sel_day.deals[list(self.sel_day.deals.keys())[0]]
        
        self.root.mainloop()

    def day_change_react(self):
        t = list(map(int, self.day_list.curselection()))
        if len(t) > 0:
            self.sel_day = self.days[t[0]]

        self.task_list.delete(0, END)
        for i in self.sel_day.deals:
            self.task_list.insert(END, ('+' if self.sel_day.deals[i]['completed'] else '-')+self.sel_day.deals[i]['deal'].name)

    def delete_task(self):
        t = list(map(int, self.task_list.curselection()))
        self.task_list.delete(t[0])
        self.refresh_cur_task()

    def refresh_cur_day(self):
        t = list(map(int, self.day_list.curselection()))
        if len(t) > 0:
            self.sel_day = self.days[t[0]]

    def refresh_cur_deal(self):
        t = list(map(int, self.task_list.curselection()))
        if len(t) > 0:
            self.sel_deal = self.sel_day.deals[self.task_list.get(t[0])[1:]]

    def show_info(self):
        self.refresh_cur_deal()
        self.refresh_cur_day()
        temp = Tk()
        temp.geometry('400x100+500+300')
        temp.title(self.sel_deal['deal'].name)
        
        temp.resizable(False, False)

        s = ''
        s += 'Name: ' + '\t' + self.sel_deal['deal'].name+'\n'
        s += 'Description: \t' + self.sel_deal['deal'].desc + '\n'
        s += 'Completed: \t' + ('Yes' if self.sel_deal['completed'] else 'No') + '\n'
        Label(temp, text=s, width=399).pack()
        
        temp.mainloop()

    def show_day_info(self):
        temp = Tk()
        self.refresh_cur_deal()
        self.refresh_cur_day()
        temp.geometry('400x100+500+300')

        temp.title(str(self.sel_day))
        
        temp.resizable(False, False)

        def stars(x):
            r = ''
            for x in range(round(x)):
                r += '★'
            for x in range(5-len(r)):
                r += '☆'
            return r
        
        s = ''
        s += 'Date: ' + '\t' + str(self.sel_day) +'\n'
        s += 'Net value: \t' + str(stars(self.sel_day.get_net_value())) + '\n'
        t = ('Yes' if len([x for x in self.sel_day.deals.keys() if not self.sel_day.deals[x]['completed']]) == 0 else 'No')
        s += 'Completed: \t' + t + '\n'
        Label(temp, text=s, width=399).pack()
        
        temp.mainloop()


    def check_deal(self):
        self.refresh_cur_deal()
        self.refresh_cur_day()

        self.sel_deal['completed'] = not self.sel_deal['completed']
        self.day_change_react()

    def graph_day(self):
        pass

# ★ ☆

a = Deal('new deal', 3, 2)
day = Day(date.today())
day.add_deal(a)
day.add_deal(Deal('drink water', 1, 2, desc='drinking is very tasty'), True)
day.add_deal(Deal('buy milk', 2, 4, desc='milk is healthy'), False)
DayVisualiser(Day.objects)
