import pandas as pd
import matplotlib.pyplot as plt

xcl = pd.ExcelFile('https://docs.google.com/spreadsheets/d/e/2PACX-1vTOZPXrV1XqR344xWaWpbfYz72eh_rLH1U1qWWClyy6yI246H9tC_24JBr2Z6hoVrJWTNJuaqE_bxmN/pub?output=xlsx')


def dialog_window():
    while True:
        print("\nWhat do I need to do?:")
        print("1.Update 1 day (chest_and_triceps)")
        print("2.Update 2 day (back_and_biceps)")
        print("3.Update 3 day (legs_and_shoulders)")
        print("4.Update all 3 days")
        print("5.Update if needed an update (doesn't work rn)")
        print("q.Quit to save the changes")
        update_number = input(">> ")
        if update_number.isdigit() and 5 >= int(update_number) >= 1:
            if int(update_number) == 1:
                update_workout('CHEST & TRICEPS')
                print('First Day Updated')
            elif int(update_number) == 2:
                update_workout('BACK & BICEPS')
                print('Second Day Updated')
            elif int(update_number) == 3:
                update_workout('LEGS & SHOULDERS')
                print('Third Day Updated')
            elif int(update_number) == 4:
                update_workout('CHEST & TRICEPS')
                print('First Day Updated')
                update_workout('BACK & BICEPS')
                print('Second Day Updated')
                update_workout('LEGS & SHOULDERS')
                print('Third Day Updated')
            # TODO: the possibility of only updating the WO that weren't been updated, saving the number of updated WO
            # elif int(update_number) == 5:
            #     if_needed_the_update()
        elif update_number.lower() == "q" or update_number == "6":
            print("quit\n")
            break
        else:
            print("wrong input\n")
    writing_down_count()


def if_needed_the_update():
    with open('count_of_days.txt') as txt:
        lines = txt.readlines()
    txt.close()
    lines[0] = lines[0].split(":")
    lines[1] = lines[1].split(":")
    lines[2] = lines[2].split(":")
    first_day = pd.read_excel(xcl, 'CHEST & TRICEPS')
    second_day = pd.read_excel(xcl, 'BACK & BICEPS')
    third_day = pd.read_excel(xcl, 'LEGS & SHOULDERS')
    if int(lines[0][1]) != first_day.shape[0]:
        update_workout('CHEST & TRICEPS')
        print('First Day Updated')
    if int(lines[1][1]) != second_day.shape[0]:
        update_workout('BACK & BICEPS')
        print('Second Day Updated')
    if int(lines[2][1]) != third_day.shape[0]:
        update_workout('LEGS & SHOULDERS')
        print('Third Day Updated')


def update_workout(wo_type):
    day = pd.read_excel(xcl, wo_type)
    height = {}
    height.update(redirection(day, height))
    saving_figure(height, wo_type)


def saving_figure(height, wo_type):
    width = 0.8
    for exercise in height.items():
        date_and_reps = exercise[1]
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(20, 10))
        keys_list = list(date_and_reps.keys())
        for i, d in enumerate(date_and_reps.values()):
            for j, ax in enumerate([ax1, ax2, ax3, ax4]):
                bar_data = [d[j]]
                ax.bar(i, bar_data, color=f'C{i}', edgecolor='white', width=width)
                for k, v in enumerate(bar_data):
                    ax.text(i, v + 1, str(v), ha='center', va='bottom')
                    ax.set_title(f'set: {j}')

            fig.legend(labels=keys_list, loc='upper left', fontsize='medium', ncols=1)

        if wo_type == 'CHEST & TRICEPS':
            plt.savefig(f'figures/chest_and_triceps/{exercise[0]}.png')
        elif wo_type == 'BACK & BICEPS':
            plt.savefig(f'figures/back_and_biceps/{exercise[0]}.png')
        else:
            plt.savefig(f'figures/legs_and_shoulders/{exercise[0]}.png')

        plt.close()


def redirection(sheet, height):
    for start, column_name in enumerate(sheet.columns):
        if "Unnamed" not in column_name and column_name != "weight":
            height.update({column_name: {}})
            for rows in range(len(sheet.index)):
                height[column_name].update({sheet.values[rows][0]: count_kgs_together(sheet, rows, start, start + 4)})
    return height


def count_kgs_together(sheet, row, start_cell, end_cell):
    array_of_equations = []
    array = []
    for x in range(start_cell, end_cell):
        array_of_equations.append(sheet.values[row][x])
    for equation in array_of_equations:
        parts = equation.split('*')
        numbers = [float(part) for part in parts]
        array.append(int(numbers[0] * numbers[1]))
    return array


def writing_down_count():
    first_day = pd.read_excel(xcl, 'CHEST & TRICEPS')
    second_day = pd.read_excel(xcl, 'BACK & BICEPS')
    third_day = pd.read_excel(xcl, 'LEGS & SHOULDERS')
    with open('count_of_days.txt', 'w') as txt:
        txt.writelines(
            ['chest_and_triceps:', str(first_day.shape[0]), '\n', 'back_and_biceps:', str(second_day.shape[0]), '\n',
             'legs_and_shoulders:', str(third_day.shape[0])])
    txt.close()


dialog_window()
