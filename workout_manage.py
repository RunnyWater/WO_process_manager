import pandas as pd
import matplotlib.pyplot as plt
import os

# You can change it to yours XCL file, if it has the same structure, as does this, it will work as good as it normally does
link_to_xcl = 'https://docs.google.com/spreadsheets/d/1b0plqR5RodygHOkzW2pEYDcle3SSPAS-0mcqIkvEljg/edit?usp=sharing'
xcl = pd.ExcelFile(link_to_xcl)


def dialog_window():
    # TODO: the possibility of only updating the WO that weren't been updated, saving the number of updated WO
    while True:
        print("\nWhat do I need to do?:")
        print("0.Update all days")
        for num, sheet in enumerate(xcl.sheet_names):
            print(f"{num + 1}.Update {num + 1} day ({sheet})")
        # print("5.Update if needed an update (doesn't work rn)")
        print("q.Quit to save the changes")
        update_number = input(">> ")
        if update_number.isnumeric and int(update_number) <= xcl.sheet_names.length and int(update_number)>=0:
            if int(update_number) == 0:
                for num, sheet in enumerate(xcl.sheet_names):
                    update_workout(sheet)
                    print(f'{num} Day Updated')
            else:
                update_workout(xcl.sheet_names[int(update_number)-1])
                print(f'\"{xcl.sheet_names[int(update_number)-1]}\" Day Updated')
        elif update_number.lower() == "q":
                print("quit\n")
                break
        else:
            print("wrong input\n")


def update_workout(wo_type):
    day = pd.read_excel(xcl, wo_type)
    height = {}
    height.update(redirection(day, height))
    saving_figure(height, wo_type)


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
        try:
            os.path.exists(os.path.join(os.path.dirname(__file__), "figures"))
        except OSError:
            os.mkdir(os.path.join(os.path.dirname(__file__), "figures"))
        finally:
            try:
                plt.savefig(f'figures/{wo_type}/{exercise[0]}.png')
            except OSError:
                os.mkdir(f'figures/{wo_type}')
            finally:
                plt.savefig(f'figures/{wo_type}/{exercise[0]}.png')

        plt.close()


dialog_window()
