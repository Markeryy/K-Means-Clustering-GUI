from tkinter import *
from tkinter import messagebox
import random
import math
from pandas import * 
from matplotlib import pyplot as plt  # matplotlib used for the plots
from copy import deepcopy

# read input file return a dictionary of inputs
def read_input(input_file):
    data = {}

    # read file
    with open(input_file, mode="r") as file:
        column_names = file.readline()
        column_names = column_names.split(",")

        # clean the column names
        for i in range(len(column_names)):
            column_names[i] = column_names[i].strip()
            data[column_names[i]] = []
        
        # get the content from column names
        for line in file:
            splitted = line.split(",")
            for i in range(len(column_names)):
                data[column_names[i]].append(float(splitted[i]))

    return data

# clear output
def clear_output():
    plt.close()
    textbox.delete(0.0, "end")  # clear textbox

# write output given a string
def write_output(output_str):
    with open("output.csv", mode="w") as file:
        file.write(output_str)

# function to get the distance of two points
def get_distance(tuple_point, tuple_cluster):
    to_square_rt = 0.0
    for i in range(len(tuple_point)):  
        to_square_rt += (tuple_point[i] - tuple_cluster[i])**2
    distance = math.sqrt(to_square_rt)
    return distance

# run when run button is clicked
def run_algo():
    # if invalid
    if chemical1.get() == chemical2.get():
        print("INVALID!")
        messagebox.showerror("showerror", "Error")
        plt.close()
    else:
        plt.clf()  # clear existing plot
        textbox.delete(0.0, "end")  # clear textbox

        # get the data
        data1 = data[chemical1.get()]
        data2 = data[chemical2.get()]
        k = k_cluster.get()

        centroids = []

        # choose k clusters (unique)
        chosen_x = []
        for i in range(k):
            x = random.randint(0, len(data1)-1)  # choose a random index
            while x in chosen_x:
                x = random.randint(0, len(data1)-1)
            chosen_x.append(x)
            centroids.append((data1[x], data2[x]))  # append the tuple of coordinates

        # initialize the points
        points = []
        for i in range(len(data1)):
            points.append((data1[i], data2[i]))

        # centroids = list of (x,y)
        # points = list of (x,y)

        # get the distances
        distances = []
        for i in range(len(points)):
            distances.append([])
            for j in range(k):
                distances[i].append(get_distance(points[i], centroids[j]))

        # print("POINTS")
        # print(points)

        # print("DISTANCES")
        # print(distances)

        # distances = [(dist cluster1, dist cluster2, ...)]

        # get the index of minimum
        # get the cluster classification of the points (same index as points)
        cluster_classification = []
        for i in range(len(points)):
            cluster_classification.append(distances[i].index(min(distances[i])))

        # print("CLUSTER CLASSIFICATION")
        # print(cluster_classification)

        # cluster points by their index cluster
        clustered_points = []
        for i in range(k):  # initialize clustered points
            clustered_points.append([])
    
        for i in range(len(points)):
            clustered_points[cluster_classification[i]].append(points[i])  # points

        # print("CLUSTERED!")
        # print(clustered_points)

        # initialize x and y coordinates
        x_coors = []
        y_coors = []
        for i in range(len(clustered_points)):
            x_coors.append([])
            y_coors.append([])

        # get the x and y coordinates (2dlist) per cluster
        for i in range(len(clustered_points)):
            for j in range(len(clustered_points[i])):
                x_coors[i].append(clustered_points[i][j][0])
                y_coors[i].append(clustered_points[i][j][1])

        # print("X")
        # print(x_coors)  # 2d list of coordinates per cluster
        # print("Y")
        # print(y_coors)

        colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']

        # main loop
        iterations = 0
        while True:
            previous_centroids = deepcopy(centroids)

            # update centroid
            for i in range(len(centroids)):
                new_x = sum(x_coors[i])/len(x_coors[i])
                new_y = sum(y_coors[i])/len(y_coors[i])
                centroids[i] = (new_x, new_y)

            # check if algorithm is done
            if previous_centroids == centroids:
                print(f"ITERATIONS: {iterations}")
                break

            iterations += 1

            # get the distances
            distances = []
            for i in range(len(points)):
                distances.append([])
                for j in range(k):
                    distances[i].append(get_distance(points[i], centroids[j]))

            # get the index of minimum
            # get the cluster classification of the points (same index as points)
            cluster_classification = []
            for i in range(len(points)):
                cluster_classification.append(distances[i].index(min(distances[i])))
            
            # cluster points by their index cluster
            # clustered_points = [
            #   [(x,y), (x,y)],   ---- cluster 0
            #   [(x,y), (x,y)],   ---- cluster 1
            #   [(x,y), (x,y)],   ---- cluster 2
            # ]
            clustered_points = []
            for i in range(k):  # initialize clustered points
                clustered_points.append([])

            for i in range(len(points)):
                clustered_points[cluster_classification[i]].append(points[i])  # points

            # initialize x and y coordinates
            x_coors = []
            y_coors = []
            for i in range(len(clustered_points)):
                x_coors.append([])
                y_coors.append([])

            # get the x and y coordinates (2dlist) per cluster
            for i in range(len(clustered_points)):
                for j in range(len(clustered_points[i])):
                    x_coors[i].append(clustered_points[i][j][0])
                    y_coors[i].append(clustered_points[i][j][1])

        # centroids = [(), ()]
        # create an output str
        output_str = ""
        for i in range(len(centroids)):
            print(f"Centroid {i}: {centroids[i]}")
            output_str += f"Centroid {i}: {centroids[i]}\n"
            for j in range(len(clustered_points[i])):
                print(f"[{clustered_points[i][j][0]}, {clustered_points[i][j][1]}]")
                output_str += f"[{clustered_points[i][j][0]}, {clustered_points[i][j][1]}]\n"
            print()
            output_str += "\n"

        textbox.insert(0.0, output_str)  # display output to textbox
        write_output(output_str)  # write output to file

        # clustered points[0] = list of points [(1, 2), (3, 4)]
        # scatter plot
        for i in range(len(clustered_points)):
            plt.scatter(x_coors[i], y_coors[i], c=colors[i])  # takes list to plot, and string color
        plt.tight_layout()  # add padding to plot
        plt.xlabel(chemical1.get())  # set plot labels
        plt.ylabel(chemical2.get())
        plt.savefig('scatterplot.png')  # save scatterplot to file
        plt.show()
        


        

            
            

    


# data dictionary containing the values given a column key
data = read_input("data/Wine.csv")







#    _____ _    _ _____ 
#   / ____| |  | |_   _|
#  | |  __| |  | | | |  
#  | | |_ | |  | | | |  
#  | |__| | |__| |_| |_ 
#   \_____|\____/|_____|
        

# set root          
root = Tk()
root.title("K Means Clustering")

# drop down boxes
chemical1 = StringVar()  # initialize string to catch value
chemical2 = StringVar()
k_cluster = IntVar()

chemical1.set(list(data.keys())[0])   # set a default value
chemical2.set(list(data.keys())[1])
k_cluster.set(2)

drop1_label = Label(root, text="Select Attributes 1")
drop1_label.grid(row=0, column=0)
drop1 = OptionMenu(root, chemical1, *data.keys())  # create a drop box
drop1.grid(row=0, column=1, sticky="W")

drop2_label = Label(root, text="Select Attributes 2")
drop2_label.grid(row=1, column=0)
drop2 = OptionMenu(root, chemical2, *data.keys())  # create a drop box
drop2.grid(row=1, column=1, sticky="W")

drop3_label = Label(root, text="Select n clusters")
drop3_label.grid(row=2, column=0)
drop3 = OptionMenu(root, k_cluster, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)  # create a drop box
drop3.grid(row=2, column=1, sticky="W")

# run button
run_button = Button(root, width=10, text="RUN", command=run_algo)
run_button.grid(row=3, column=0, sticky="W")

# clear button
clear_button = Button(root, width=10, text="CLEAR", command=clear_output)
clear_button.grid(row=3, column=1, sticky="W")

textbox_label = Label(root, text="Centroids & Clusters")
textbox_label.grid(row=4, column=0)
# output viewer
scrollbar = Scrollbar(root)
textbox = Text(root, height=40, width=60, yscrollcommand=scrollbar.set)
textbox.grid(row=4, column=1)










root.mainloop()