import pandas as pd
import matplotlib.pyplot as plt
import os


# You can change it to yours XCL file, if it has the same structure, as does this, it will work as good as it normally does
file_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTOZPXrV1XqR344xWaWpbfYz72eh_rLH1U1qWWClyy6yI246H9tC_24JBr2Z6hoVrJWTNJuaqE_bxmN/pub?output=xlsx'
xcl = pd.ExcelFile(file_url, engine='openpyxl')


def dialog_window():
    # TODO: the possibility of only updating the WO that weren't been updated, saving the number of updated WO
    while True:
        print("\nWhat do I need to do?:")
        print("0.Update all days")
        for num, wo_type in enumerate(xcl.sheet_names):
            print(f"{num + 1}.Update {num + 1} day ({wo_type})")
        # print("5.Update if needed an update (doesn't work rn)")
        print("q.Quit to save the changes")
        update_number = input(">> ")
        if update_number.lower() == "q":
            print("quit\n")
            break
        elif update_number.isnumeric() and len(xcl.sheet_names) >= int(update_number) >= 0:
            if int(update_number) == 0:
                for num, wo_type in enumerate(xcl.sheet_names):
                    update_workout(wo_type)
                    print(f'"{wo_type}" Day Updated')
            else:
                update_workout(xcl.sheet_names[int(update_number)-1])
                print(f'\"{xcl.sheet_names[int(update_number)-1]}\" Day Updated')
        else:
            print("wrong input\n")


def update_workout(wo_type):
    day = pd.read_excel(xcl, wo_type)
    height = {}
    height.update(redirection(day, height))
    saving_figure(height, wo_type)


def redirection(wo_type, height):
    for start, column_name in enumerate(wo_type.columns):
        if "Unnamed" not in column_name and column_name != "weight":
            height.update({column_name: {}})
            final = find_final(start, wo_type)
            for rows in range(len(wo_type.index)):
                height[column_name].update({wo_type.values[rows][0]: count_kgs_together(wo_type, rows, start, final)})
    return height


def find_final(start, wo_type):
    for final, column_name in enumerate(wo_type.columns):
        if final > start and "Unnamed" not in column_name:
            return final


def count_kgs_together(wo_type, row, start_cell, end_cell):
    array_of_equations = []
    array = []
    for x in range(start_cell, end_cell):
        array_of_equations.append(wo_type.values[row][x])
    for equation in array_of_equations:
        parts = equation.split('*')
        numbers = [float(part) for part in parts]
        array.append(int(numbers[0] * numbers[1]))
    return array


def saving_figure(height, wo_type):
    folder_name = 'figures'
    main_dir = os.path.join(os.path.dirname(__file__), folder_name)
    if not os.path.exists(main_dir):
        os.mkdir(main_dir)
    sub_dir = os.path.join(main_dir, wo_type)
    if not os.path.exists(sub_dir):
        os.mkdir(sub_dir)
    width = 0.8
    colors = [f'C{i}' for i in range(len(pd.read_excel(xcl, wo_type).index))]
    for exercise_name, date_and_reps in height.items():
        num_sets = len(next(iter(date_and_reps.values())))
        fig, axs = plt.subplots(1, num_sets, figsize=(5 * num_sets, 10))

        if num_sets == 1:
            axs = [axs]

        keys_list = list(date_and_reps.keys())

        for i, reps in enumerate(date_and_reps.values()):
            for j in range(num_sets):
                bar_data = [reps[j]]
                axs[j].bar(i, bar_data, color=colors[i], edgecolor='white', width=width)
                for v in bar_data:
                    axs[j].text(i, v + 1, str(v), ha='center', va='bottom')
                axs[j].set_title(f'set: {j + 1}')  # add 1 to set number for 1-based indexing

        fig.legend(labels=keys_list, loc='upper left', fontsize='medium', ncols=1)
        plt.savefig(os.path.join(sub_dir, f'{exercise_name}.png'))
        plt.close()


dialog_window()
