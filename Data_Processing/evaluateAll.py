'''
This Script is intended to convert datasets of synthetic sharks into yolo compatible datasets
'''
# Imports
import argparse
import os
from ultralytics import YOLO
import pickle
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
matplotlib.use('Qt5Agg')

# Defaults for use as a script
dtgt = "C:\\Users\\dylan\\Documents\\Data\\YSP_Training_Results\\cleaned\\"
ddst = "C:\\Users\\dylan\\Documents\\Data\\YSP_Training_Results\\evals"
ddt = "C:\\Users\\dylan\\Documents\\Shark_Spotting_w_YOLOv8\\datasets\\data_test.yaml"

# Title Dict
title_dict = {'200_Epoch_B32':'Batch Size:32', 'Batch16':'Batch Size:16', 'cls_gain5.5':'Class Gain Increase',
              'custom_data':'Added Custom Data', 'default_100_aug':'Preaugmentation',
              'default_100_epochs':'Default for 100 Epochs', 'epoch200_B8':'Batch Size:8',
              'long_train':'Train for 500 Epochs', 'long_warmup':'Double Warmup',
              'lr0_0.001':'Decrease Learning Rate x10',
              'lr0_5.5':'Increase Learning Rate x5', 'med200_B8':'Medium Model',
              'momentum0.99':'Increased Momentum',
              'more_aug':'More Built In Augmentation', 'more_aug_new_data':'More Aug w/ Additional Data',
              'no_aug_params':'No Augmentation', 'no_warmup':'No Warmup', 'small200_B8':'Small Model',
              'tiny_batch':'Batch Size:4'}

'''Function to add arguments'''
def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tgt', type=str, default=dtgt, help='Path to results')
    parser.add_argument('--dst', type=str, default=ddst, help='Path to save')
    parser.add_argument('--data', type=str, default=ddt, help='Path to save')
    return parser

'''Main function'''
def main_func(args):
    # Get a list of all the results directories
    result_dirs = os.listdir(args.tgt)

    # For each directory, if it has a weights folder run evaluation
    eval_res = []
    exps = []
    train_data = []
    for exp in result_dirs:
        res_path = os.path.join(args.tgt, exp)
        dest_path = os.path.join(args.dst, exp)
        if os.path.isdir(res_path) \
                and os.path.exists(os.path.join(res_path,"weights")) \
                and not os.path.exists(dest_path):
            weights_path = os.path.join(res_path,"weights\\best.pt")
            # Evaluate Model
            model = YOLO(weights_path)
            result = model.val(args.data, project=args.dst, name=exp)
            # Write Results to File
            write_to_file(result, os.path.join(dest_path, exp+"_results.pickle"))
            eval_res.append(result)
            exps.append(exp)
            csv_path = pd.read_csv(os.path.join(res_path, "results.csv"))
            train_data.append(csv_path)
        else:
            result = read_from_file(os.path.join(dest_path, exp+"_results.pickle"))
            eval_res.append(result)
            exps.append(exp)
            csv_path = pd.read_csv(os.path.join(res_path, "results.csv"))
            train_data.append(csv_path)

    # Replace Names
    replaceWithDict(exps, title_dict)

    # Build Lists
    P = []
    R = []
    mAP50 = []
    mAPtrain = []
    ptrain = []
    P_Shark = []
    R_Shark = []
    mAP50_Shark = []
    P_Boat = []
    R_Boat = []
    mAP50_Boat = []
    P_Person = []
    R_Person = []
    mAP50_Person = []
    P_SeaL = []
    R_SeaL = []
    mAP50_SeaL = []
    for exp, res, tdata in zip(exps, eval_res, train_data):
        ptrain.append(tdata['   metrics/precision(B)'])
        mAPtrain.append(tdata['       metrics/mAP50(B)'])
        mAP50.append(res.results_dict['metrics/mAP50(B)'])
        P.append(res.results_dict['metrics/precision(B)'])
        R.append(res.results_dict['metrics/recall(B)'])
        P_Shark.append(res.box.p[3])
        R_Shark.append(res.box.p[3])
        mAP50_Shark.append(res.box.r[3])
        P_Boat.append(res.box.p[0])
        R_Boat.append(res.box.p[0])
        mAP50_Boat.append(res.box.r[0])
        P_Person.append(res.box.p[1])
        R_Person.append(res.box.p[1])
        mAP50_Person.append(res.box.r[1])
        P_SeaL.append(res.box.p[2])
        R_SeaL.append(res.box.p[2])
        mAP50_SeaL.append(res.box.r[2])


    top3 = find_largest_indices(P)
    top3_exp = ind2sublist(exps, top3)
    top3_P = ind2sublist(P, top3)
    top3_mAP = ind2sublist(mAP50, top3)
    top3_mAPtrain = ind2sublist(mAPtrain, top3)

    bot3 = find_smallest_indices(P)
    bot3_exp = ind2sublist(exps, bot3)
    bot3_P = ind2sublist(P, bot3)
    bot3_mAP = ind2sublist(mAP50, bot3)
    bot3_mAPtrain = ind2sublist(mAPtrain, bot3)

    top3_shark = find_largest_indices(mAP50_Shark)
    top3_shark_exp = ind2sublist(exps, top3_shark)
    top3_shark_P = ind2sublist(P, top3_shark)
    top3_shark_mAP = ind2sublist(mAP50, top3_shark)
    top3_shark_mAPtrain = ind2sublist(mAPtrain, top3_shark)


    # Graph all Precision and Recall
    visualize_double_performance(exps, P, R,
                                 title='All Runs Precision and Recall', ylabel='Precision(left)/Recall(right)', save_dir=args.dst)
    # Graph all mAP50
    visualize_model_performance(exps, mAP50, title='All Runs mAP50', ylabel='mAP50', save_dir=args.dst)
    # Graph All Training Runs
    visualize_model_performance(exps, P, title='All Training Runs mAP50', ylabel='mAP50', save_dir=args.dst)
    # Graph all Shark Precision
    visualize_model_performance(exps, P_Shark, title='All Training Runs Precision Sharks', ylabel='mAP50',
                                save_dir=args.dst)
    # Graph all Shark mAP
    visualize_model_performance(exps, mAP50_Shark, title='All Training Runs mAP50 Sharks', ylabel='mAP50',
                                save_dir=args.dst)

    # Graph Top 3 Training Runs
    visualize_model_performance(top3_exp, top3_P, title='Top 3 Runs Precision', ylabel='mAP50', save_dir=args.dst)
    # Graph Bottom 3 Training Runs
    visualize_model_performance(bot3_exp, bot3_P, title='Bottom 3 Runs Precision', ylabel='mAP50', save_dir=args.dst)
    # Graph Top 3 Training Runs
    visualize_model_performance(top3_exp, top3_mAP, title='Top 3 Runs mAP50', ylabel='mAP50', save_dir=args.dst)
    # Graph Bottom 3 Training Runs
    visualize_model_performance(bot3_exp, bot3_mAP, title='Bottom 3 Runs mAP50', ylabel='mAP50', save_dir=args.dst)
    # Graph All Training Runs
    plot_series(exps, mAPtrain, title='All Training Runs mAP50', xlabel='Epochs', ylabel='mAP50', save_dir=args.dst)
    # Graph mAP50 of top 3
    plot_series(top3_exp, top3_mAPtrain, title='Top 3 Training Runs mAP50', xlabel='Epochs', ylabel='mAP50', save_dir=args.dst)
    # Graph P of top 3
    plot_series(bot3_exp, bot3_mAPtrain, title='Bottom 3 Training Runs mAP50', xlabel='Epochs', ylabel='mAP50', save_dir=args.dst)
    # Top 3 Sharks
    visualize_model_performance(top3_shark_exp, top3_shark_P, title='Top 3 Runs mAP50 (Sharks)', ylabel='mAP50', save_dir=args.dst)

    # Graph Training Runs of Batch Sizes:
    batches_names, batches_vals = find_subset(exps, mAPtrain, ['Batch Size:4', 'Batch Size:8', 'Batch Size:16', 'Batch Size:32'])
    plot_series(batches_names, batches_vals, title='Batch Runs', xlabel='Epochs', ylabel='mAP50',
                save_dir=args.dst)
    # Graph Training Runs of LR
    lr_names, lr_vals = find_subset(exps, mAPtrain,
                                              ['Batch Size:32', 'Decrease Learning Rate x10', 'Increase Learning Rate x5'])
    plot_series(lr_names, lr_vals, title='Learning Rate Runs', xlabel='Epochs', ylabel='mAP50',
                save_dir=args.dst)
    # Augmentation
    aug_names, aug_vals = find_subset(exps, mAPtrain,
                                    ['Batch Size:32', 'No Augmentation', 'More Built In Augmentation',
                                     'More Aug w/ Additional Data', 'Preaugmentation'])
    plot_series(aug_names, aug_vals, title='Augmentation mAP Runs', xlabel='Epochs', ylabel='mAP50',
                save_dir=args.dst)
    # Warmup
    wr_names, wr_vals = find_subset(exps, mAPtrain,
                                      ['Batch Size:32', 'Double Warmup', 'No Warmup'])
    plot_series(wr_names, wr_vals, title='Warmup mAP Runs', xlabel='Epochs', ylabel='mAP50',
                save_dir=args.dst)
    # Model Size
    sz_names, sz_vals = find_subset(exps, mAPtrain,
                                    ['Batch Size:32', 'Small Model', 'Medium Model'])
    plot_series(sz_names, sz_vals, title='Model Size Runs', xlabel='Epochs', ylabel='mAP50',
                save_dir=args.dst)
    # Misc
    mom_names, mom_vals = find_subset(exps, mAPtrain,
                                    ['Batch Size:32', 'Increased Momentum', 'Default for 500 Epochs'])
    plot_series(mom_names, mom_vals, title='Misc Training Runs', xlabel='Epochs', ylabel='mAP50',
                save_dir=args.dst)

    print("Done!")


def find_subset(A, B, C):
    # Find the values in A that are in C
    common_vals = set(A).intersection(set(C))

    # Create a list of the indices of common values in A
    common_indices = [i for i in range(len(A)) if A[i] in common_vals]

    # Use the common indices to create the subsets of A and B
    subset_A = [A[i] for i in common_indices]
    subset_B = [B[i] for i in common_indices]

    # Return the subsets
    return subset_A, subset_B

def ind2sublist(lst, inds):
    return [lst[i] for i in inds if i < len(lst)]

def write_to_file(obj, filename):
    with open(filename, 'wb') as file:
        pickle.dump(obj, file)

def read_from_file(filename):
    with open(filename, 'rb') as file:
        obj = pickle.load(file)
    return obj

def find_largest_indices(lst):
    indices = sorted(range(len(lst)), key=lambda i: lst[i], reverse=True)
    return indices[:3]
def find_smallest_indices(lst):
    indices = sorted(range(len(lst)), key=lambda i: lst[i], reverse=True)
    return indices[-3:]

def replaceWithDict(list, dict):
    for i in range(len(list)):
        if list[i] in dict:
            list[i] = dict[list[i]]


def visualize_model_performance(model_names, precision_values, title='', ylabel='', save_dir='', show=False):
    # create a bar chart of the precision values for each model
    fig, ax = plt.subplots(figsize=(8,6))
    bars = ax.bar(model_names, precision_values)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    # add the precision value vertically on top of each bar
    for bar, precision in zip(bars, precision_values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height()-0.3, f"{precision:.2f}", color='white',
                ha='center', va='center', rotation='vertical')
    # adjust the margins to fit the x-axis labels
    plt.subplots_adjust(bottom=0.3)
    # rotate the x-axis labels for readability
    plt.xticks(rotation=45, ha='right')
    if show:
        plt.show()
    if save_dir != '' and title != '':
        plt.savefig(os.path.join(save_dir, title+".png"))

def visualize_double_performance(experiment_names, metric1_values, metric2_values, title='', xlabel = '', ylabel='',
                                 save_dir='', show=False):
    # Set the width of each bar
    bar_width = 0.35

    # Set the x coordinates for the left side of each bar
    x_pos = range(len(experiment_names))

    # Create the figure and axis objects
    fig, ax = plt.subplots()

    # Create two bars for each experiment
    rects1 = ax.bar(x_pos, metric1_values, width=bar_width, color='tab:blue', label='')
    rects2 = ax.bar([x + bar_width for x in x_pos], metric2_values,
                    width=bar_width, color='tab:orange', label='')

    # Add labels and title to the graph
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks([x + bar_width/2 for x in x_pos])
    ax.set_xticklabels(experiment_names, rotation=90)

    # Add a legend to the graph
    ax.legend()

    # Add the metric values as text labels above the bars
    for i in range(len(rects1)):
        ax.text(rects1[i].get_x() + rects1[i].get_width()/2, rects1[i].get_height() - 0.3, f"{metric1_values[i]:.2f}",
                ha='center', va='center', color='white', rotation='vertical')
        ax.text(rects2[i].get_x() + rects2[i].get_width()/2, rects2[i].get_height() - 0.3, f"{metric1_values[i]:.2f}",
                ha='center', va='center', color='white', rotation='vertical')
    plt.subplots_adjust(bottom=0.3)
    # Display the graph
    if show:
        plt.show()
    if save_dir != '' and title != '':
        plt.savefig(os.path.join(save_dir, title+".png"))

def plot_series(experiment_names, series_list, title='', xlabel = '', ylabel='', save_dir='', show=False):
    fig, ax = plt.subplots(figsize=(8,6))
    for i, series in enumerate(series_list):
        x = range(1, len(series)+1)
        ax.plot(x, series, label=experiment_names[i])
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.subplots_adjust(right=0.7)
    plt.grid()
    if show:
        plt.show()
    if save_dir != '' and title != '':
        plt.savefig(os.path.join(save_dir, title+".png"))


if __name__ == '__main__':
    args =  init_parser().parse_args()
    print(args)
    main_func(args)
