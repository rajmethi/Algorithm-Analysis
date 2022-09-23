import time, pygame, random, queue, util
#sorting algs: quicksort, selection, insertion, bubble, merge, binary


mazev2 = []
#0 = wall, 1 = space
mazev2.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
mazev2.append([0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0])
mazev2.append([0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
mazev2.append([0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0])
mazev2.append([0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0])
mazev2.append([0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0])
mazev2.append([0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0])
mazev2.append([0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0])
mazev2.append([0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0])
mazev2.append([0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0])
mazev2.append([0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0])
mazev2.append([0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0])
mazev2.append([0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
mazev2.append([0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0])
mazev2.append([0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0])
mazev2.append([0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0])
mazev2.append([0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0])
mazev2.append([0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0])
mazev2.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

#graph-nodes: each node functions as a space on the 19x19 maze (not states of solving)
class Node:

    def __init__(self, key):
        self.key = key
        self.neighbors = {}
        self.neighbors_set = set() #prevent dupes


    def add_neighbor(self, node, weight):
        if node not in self.neighbors_set:
            self.neighbors[node.key] = weight #weight unused;
            node.neighbors[self.key] = weight
            self.neighbors_set.add(node)
            node.neighbors_set.add(self)

    def __str__(self):
        s = "ID: " + self.key + "\nNeighbors: "
        for n in self.neighbors:
            s += n + ":" + str(self.neighbors[n]) + "  "
        return s

    def __lt__(self, other):
        return self.key < other.key #unused method


class Graph:
    def __init__(self):
        self.graph = {}

    def add_node(self, node):
        self.graph[node.key] = node

    def add_edge(self, node1, node2, weight): #technically arbitrary considering add_neighbor()...
        if not node1.key in self.graph:
            print("Node with ID " + node1.key + " is not in the graph")
        elif not node2.key in self.graph:
            print("Node with ID " + node2.key + " is not in the graph")
        else:
            node1.add_neighbor(node2, weight)

    def __str__(self):
        s = ""
        for node in self.graph:
            s += self.graph[node].__str__() + "\n\n"
        return s

    def get_path_cost(self, path): #used in console display mainly
        print(path)
        cost = 0
        for i in range(len(path) - 1):
            getnode = self.graph[path[i]]
            print(getnode)
            cost += getnode.neighbors[path[i + 1]]
        return cost

    def get_bfs_path(self, startnode, endnode):
        visited = []
        nodequeue = []
        visited.append(startnode)
        nodequeue.append((startnode, [startnode]))
        while nodequeue:
            currentnode, path = nodequeue.pop(0) #path = optimal route, currentnode is node being looked at
            if currentnode == endnode:
                visited.append(currentnode)
                return visited
            if currentnode not in visited:
                visited.append(currentnode)
            for neighbor in currentnode.neighbors_set:
                if neighbor not in visited:
                    nodequeue.append((neighbor, path + [neighbor]))
        return visited

    def get_ucs_path(self, startnode, endnode): #unused
        visited = []
        path = []
        q = queue.PriorityQueue()
        visited.append(startnode.key)
        q.put((0, startnode, [startnode.key]))
        while q:
            cost, node, path = q.get()
            if node == endnode:
                return path
            if node not in visited:
                visited.append(node)
                for neighbor in node.neighbors_set:
                    if neighbor not in visited:
                        q.put((node.neighbors[neighbor.key] + cost, neighbor, path + [neighbor.key]))
        return path

    def get_dfs_path(self, startnode, endnode):
        visited = []
        nodequeue = []
        visited.append(startnode)
        nodequeue.append((startnode, [startnode]))
        while nodequeue:
            currentnode, path = nodequeue.pop()
            if currentnode == endnode:
                visited.append(currentnode)
                return visited
            for neighbor in currentnode.neighbors_set:
                if neighbor not in visited:
                    visited.append(neighbor)
                    nodequeue.append((neighbor, path + [neighbor]))
        return visited

    def DLS(self, startnode, endnode, depth): #helper function for iterative depth search, unused.
        visited = []
        canvisit = []
        visited.append(startnode)
        canvisit.append((startnode, 0))
        while len(canvisit) > 0:
            currentnode, distance = canvisit.pop()
            if currentnode == endnode:
                return visited
            for neighbor in currentnode.neighbors_set:
                if neighbor not in visited and distance + 1 <= depth:
                    canvisit.append((neighbor, distance + 1))
                    visited.append(neighbor)
        return visited

    def get_ids_path(self, startnode, endnode, maxdepth):
        paths = []
        visited = self.DLS(startnode, endnode, maxdepth)

        for i in range(maxdepth, -1, -1):
            path = []
            nextvisited = self.DLS(startnode, endnode, i)
            for node in nextvisited:
                path.append(node.key)
            paths.append(path)

            if len(visited) == len(nextvisited):
                optimaldepth = i
        for path in paths:
            print(len(path))
        return paths

    def a_star_path(self, startnode, endnode): #unused, needs weight implementation with maze
        visited = []
        q = queue.PriorityQueue()
        q.put((0, 0, 0, startnode))
        while q.qsize() > 0:
            evalcost, costfromstart, depth, node = q.get()
            print(node.key)
            if node not in visited:
                visited.append(node)
                if node == endnode:
                    print("found")
                for neighbor in node.neighbors_set:
                    print(neighbor)
                    if neighbor not in visited:

                        heur = depth - 2
                        q.put((heur + costfromstart + node.neighbors[neighbor.key],
                               costfromstart + node.neighbors[neighbor.key], depth + 1, neighbor))
                        print(q)

#some sorting functions were made iterative, due to troubles with capturing all iterations with recursion
#note: time analyses may not be accurate in the full scope due to small list size and iteration vs recursion.
def partition_rec(list1, pivot): #used in quicksort
    lesser = []
    equal = []
    greater = []
    for item in list1:
        if item == pivot:
            equal.append(item)
        elif item < pivot:
            lesser.append(item)
        else:
            greater.append(item)
    return lesser, equal, greater
def quick_sort_rec(list1):
    if len(list1) <= 1: #base case.
        return list1

    else:
        pivotindex = random.randint(0, len(list1) - 1) #choose a random point to create 3 lists.
        lesser, equal, greater = partition_rec(list1, list1[pivotindex]) #call partition function to create 3 lists.
        return quick_sort_rec(lesser) + equal + quick_sort_rec(greater) #recursively call quicksort on larger/lesser portions
def partition_iter(list1, low, high):
    i = (low - 1)
    x = list1[high]

    for j in range(low, high):
        if list1[j] <= x:
            i = i + 1
            list1[i], list1[j] = list1[j], list1[i]

    list1[i + 1], list1[high] = list1[high], list1[i + 1]
    return (i + 1), list1
def quickSortIterative(list1):
    iterations = []
    iterations.append(list1.copy())
    high_index = len(list1) -1
    low_index = 0
    stack = [0] * len(list1)
    top = -1
    top = top + 1
    stack[top] = low_index
    top = top + 1
    stack[top] = high_index
    count = 0
    while top >= 0:
        count +=1
        high_index = stack[top]
        top = top - 1
        low_index = stack[top]
        top = top - 1
        p, mylist = partition_iter(list1, low_index, high_index)
        iteration = mylist.copy()
        iterations.append(iteration)
        if p - 1 > low_index:
            top = top + 1
            stack[top] = low_index
            top = top + 1
            stack[top] = p - 1
        if p + 1 < high_index:
            top = top + 1
            stack[top] = p + 1
            top = top + 1
            stack[top] = high_index
    end = time.time()
    return iterations
def sel_sort(mylist):
    sel_iterations = []
    for y in range(len(mylist)):
        lowIndex = y #arbitrary initial val

        for i in range(y + 1, len(mylist)):
            if mylist[i] < mylist[lowIndex]:
                lowIndex = i #find the real index of the lowest val
        lst = mylist.copy()
        sel_iterations.append(lst)
        mylist[y], mylist[lowIndex] = mylist[lowIndex], mylist[y] #switch 2 ints at one time.
    end = time.time()
    return sel_iterations
def ins_sort(mylist):

    iterations = []
    for y in range(len(mylist)):
        element = mylist[y]
        x = y - 1
        while x >= 0 and element < mylist[x]:
            mylist[x + 1] = mylist[x]
            x -= 1
        mylist[x + 1] = element

        iteration = mylist.copy()
        iterations.append(iteration)

    return iterations
def bub_sort(lst):
    iterations = []
    iteration = lst.copy()
    iterations.append(iteration)
    lastsortednum = len(lst) - 1
    for i in range(lastsortednum):

        swapped = False
        j = 0

        while j < lastsortednum:
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                swapped = True
                iteration = lst.copy()
                iterations.append(iteration)


            j += 1
        # lastsortednum-=1
    end = time.time()

    return iterations
def merge(lista, listb):
    merged = []
    while len(lista) > 0 and len(listb) > 0:
        #print(lista[0])
        #print(listb[0])
        if lista[0] < listb[0]:
            merged.append(lista.pop(0))
        else:
            merged.append(listb.pop(0))
    return merged + lista + listb
def merge_sort(list1, iterations):
    if len(list1) <= 1:
        iteration = list1.copy()
        iterations.append(iteration)
        print(iteration)
        return (list1)
    else:
        iteration = list1.copy()
        iterations.append(iteration)
        print(iteration)
        num = len(list1) // 2
        lista = merge_sort(list1[:num], iterations)
        listb = merge_sort(list1[num:], iterations)
    return merge(lista, listb)
def merge_iter(list1, temp, x, mid, end):
    k = x
    i = x
    j = mid + 1
    while i <= mid and j <= end:
        if list1[i] < list1[j]:
            temp[k] = list1[i]
            i = i + 1
        else:
            temp[k] = list1[j]
            j = j + 1
        k = k + 1
    while i < len(list1) and i <= mid:
        temp[k] = list1[i]
        k = k + 1
        i = i + 1
    for i in range(x, end + 1):
        list1[i] = temp[i]
def mergesort(mylist):
    iterations = []
    iteration = mylist.copy()
    iterations.append(iteration)
    low = 0
    high = len(mylist) - 1

    temp = mylist.copy()
    block_size = 1
    while block_size <= high - low:
        for i in range(low, high, 2 * block_size):
            start = i
            mid = i + block_size - 1
            end = min(i + 2 * block_size - 1, high)
            merge_iter(mylist, temp, start, mid, end)
        iteration = mylist.copy()
        iterations.append(iteration)
        block_size = 2 * block_size
    end = time.time()
    return iterations

def console_main():
    pass #unneeded
def graphics_main():
    pygame.init()
    win_width = 1450
    win_height = 800
    screen = pygame.display.set_mode((win_width, win_height))
    max_FPS = 60
    clock = pygame.time.Clock()
    running = True

    titlefont = pygame.font.SysFont("Helvetica", 36, True, True)
    sub_title_font = pygame.font.SysFont("Helvetica", 22, True, False)
    num_font = pygame.font.SysFont("Helvetica", 16, True, False)
    sort_font = pygame.font.SysFont("Helvetica", 22, False, True)
    title_text = titlefont.render("Algorithm Analysis", True, "White")
    screen.blit(title_text, (725 - (title_text.get_width() / 2), 0))
    rb_ss = util.RadioButton(screen, 15, 15, 15, "Sorting/Searching")
    rb_ts = util.RadioButton(screen, 15, 50, 15, "Time/Space")
    def sorting(): #create rand list, generate all iterations to prevent lag in window.
        mylist = []
        while len(mylist) < 10:
            num = random.randint(1,10)
            if num not in mylist:
                mylist.append(num)

        rand_list = mylist.copy()
        rand_list_text = sub_title_font.render("Disordered List: " + str(rand_list), True, 'White')
        screen.blit(rand_list_text, (725 - (rand_list_text.get_width() / 2), 50))

        sel_sort_list = mylist.copy()
        quick_sort_list = mylist.copy()
        ins_sort_list = mylist.copy()
        bub_sort_list = mylist.copy()
        merge_sort_list = mylist.copy()
        sel_start = time.time()
        sel_iterations= sel_sort(sel_sort_list)
        sel_end = time.time()
        quick_start = time.time()
        quick_iterations= quickSortIterative(quick_sort_list)
        quick_end = time.time()
        ins_start = time.time()
        insertion_iterations= ins_sort(ins_sort_list)
        ins_end = time.time()
        bub_start = time.time()
        bubble_iterations= bub_sort(bub_sort_list)
        bub_end = time.time()
        merge_start = time.time()
        merge_iterations = mergesort(merge_sort_list)
        merge_end = time.time()
        all_iterations = [merge_iterations,quick_iterations, insertion_iterations,sel_iterations ,bubble_iterations]  # list of lists of lists
        all_times = [(merge_end-merge_start), (quick_end-quick_start), (ins_end-ins_start), (sel_end-sel_start),(bub_end-bub_start)]
        return all_iterations, all_times
    def on_click():
        def sorting_run():
            loading_rect_left_x = 530 #no real purpose, just looks cool
            loading_rect_right_x = 910
            sort_colors = [[204, 102, 0], [153, 0, 0], [0, 0, 144], [153, 0, 76], [0, 102, 51]] #initial rgb vals for animations
            start_x_vals = [30, 315, 600, 885, 1170] #locations for each animation to start
            runtime_y_vals = [500, 530, 560, 590, 620] #location of runtime analyses
            sort_strings = ['Merge Sort         ', 'Quick Sort         ', 'Insertion Sort    ', 'Selection Sort  ',
                            'Bubble Sort     ']
            time_strings = ['Merge Sort   // O(n*logn)', 'Quick Sort    // O(n*logn)', 'Insertion Sort      // O(n2)',
                            'Selection Sort    // O(n2)', 'Bubble Sort        // O(n2)']
            space_strings = ['Merge Sort           // O(n)', 'Quick Sort           //  O(n)',
                             'Insertion Sort       //  O(1)', 'Selection Sort      //  O(1)',
                             'Bubble Sort         //  O(1)']
            pygame.display.flip()
            #MASSIVE UNZIP: iterate thru all lists at the same time.
            for sort, color, x_coord, runtime, time_string, space_string, sort_string, runtime_y in zip(all_iterations,
                                                                                                        sort_colors,
                                                                                                        start_x_vals,
                                                                                                        all_times,
                                                                                                        time_strings,
                                                                                                        space_strings,
                                                                                                        sort_strings,
                                                                                                        runtime_y_vals):
                y_coord = 100
                if rb_ts.toggled: #time/space radio in top left.
                    name_comp_string = space_string
                else:
                    name_comp_string = time_string
                row_x_set = x_coord #start location for each iteration
                sort_title_text = sort_font.render(name_comp_string, True, 'White')
                screen.blit(sort_title_text, (x_coord, y_coord - 10))
                (r, g, b) = color
                for iteration in sort:
                    loading_rect_left = (loading_rect_left_x, 5, 3, 26)
                    loading_rect_right = (loading_rect_right_x, 5, 3, 26)
                    pygame.draw.rect(screen, (r, g, b), loading_rect_left)
                    pygame.draw.rect(screen, (r, g, b), loading_rect_right)
                    loading_rect_left_x -= 5
                    loading_rect_right_x += 5
                    y_coord += 20
                    #lighten color...
                    if r + 30 <= 255:
                        r += 30
                    else:
                        r = 255
                    if g + 30 <= 255:
                        g += 30
                    else:
                        g = 255
                    if b + 30 <= 255:
                        b += 30
                    else:
                        b = 255
                    x_coord = row_x_set
                    for num in iteration:
                        line = pygame.Rect(x_coord, y_coord, 2, 12)  # divider between util/animation

                        int_text = num_font.render(str(num), True, (r, g, b))
                        if num != 10:
                            screen.blit(int_text, (x_coord + 9, y_coord))
                        else: #10 is longer than 1 digit num, so adjust
                            screen.blit(int_text, (x_coord + 3, y_coord))
                        pygame.draw.rect(screen, 'white', line)
                        x_coord += 23
                        line = pygame.Rect(x_coord, y_coord, 2, 12)  # divider between util/animation
                        pygame.draw.rect(screen, 'white', line)
                        pygame.display.update()
                runtime_text = sort_font.render(sort_string + ": " + str(runtime), True, 'White')
                screen.blit(runtime_text, (10, runtime_y))

        def searching_run():
            g = Graph()
            nodes = []
            for i in range(len(mazev2)):
                row = []
                for y in range(len(mazev2[i])):
                    row.append(Node("(" + str(i) +","+ str(y)+")")) #key for node, a string with x,y
                nodes.append(row)

            node_space_dict = {}
            count = 0
            for i in range(len(mazev2)):
                for y in range(len(mazev2[i])):
                    node_space_dict[nodes[i][y]] = mazev2[i][y] #node: wall or space

            for key in node_space_dict:
                if node_space_dict[key] == 1: #if node is not a wall,
                    for i, row in enumerate(nodes):
                        if key in row:
                            i,y = i, row.index(key) #2d list index for node
                            #check all 4 possible surrounding spots of node, and add neighbor if they are not a wall
                            if not i+ 1 > 18:
                                if mazev2[i+1][y] == 1:
                                    nodes[i][y].add_neighbor(nodes[i+1][y],1)
                            if not i -1 < 0:
                                if mazev2[i - 1][y] == 1:

                                    nodes[i][y].add_neighbor(nodes[i-1][y],1)
                            if not y + 1 > 18:
                                if mazev2[i][y + 1] == 1:
                                    nodes[i][y].add_neighbor(nodes[i][y+1],1)
                            if not y - 1 < 0:
                                if mazev2[i][y - 1] == 1:
                                    nodes[i][y].add_neighbor(nodes[i][y-1],1)
            for row in nodes:
                for node in row:
                    g.add_node(node) #update graph
            print(g)

            #print(nodes[1][14])
            bfs_path = g.get_bfs_path(nodes[1][1], nodes[17][17]) #generate visiteds.
            dfs_path = g.get_dfs_path(nodes[1][1], nodes[17][17])

            x_loc = 250
            y_loc = 200
            squares = []
            squares2 = []

            for line in mazev2:
                line_list = []
                for square in line:
                    drawn = (x_loc,y_loc, 20,20)
                    line_list.append(drawn)
                    if square == 1:
                        pygame.draw.rect(screen, 'black', drawn)
                    else:
                        pygame.draw.rect(screen, (204,0,102), drawn)

                    x_loc += 20
                squares.append(line_list)
                y_loc += 20
                x_loc = 250

            x_loc = 800
            y_loc = 200
            for line in mazev2:
                line_list = []
                for square in line:
                    drawn = (x_loc,y_loc, 20,20)
                    line_list.append(drawn)
                    if square == 1:
                        pygame.draw.rect(screen, 'black', drawn)
                    else:
                        pygame.draw.rect(screen, (0,128,255), drawn)
                    x_loc += 20
                squares2.append(line_list)
                y_loc += 20
                x_loc = 800


            dfs_text = sort_font.render("//Depth-First Search", True, 'White')
            screen.blit(dfs_text, (250, 180))
            bfs_text = sort_font.render("//Breadth-First Search", True, 'White')
            screen.blit(bfs_text, (800, 180))
            pygame.display.update()

            for i in range(len(dfs_path)):
                for i2, row in enumerate(nodes): #avoid variable conflict
                    if dfs_path[i] in row:
                        i2, y2 = i2, row.index(dfs_path[i])

                        pygame.draw.rect(screen, 'white',(squares[i2][y2]))
                        pygame.display.update()

            for i in range(len(bfs_path)):
                for i2, row in enumerate(nodes):
                    if bfs_path[i] in row:
                        i2, y2 = i2, row.index(bfs_path[i])

                        pygame.draw.rect(screen, 'white',(squares2[i2][y2]))
                        pygame.display.update()

        clear_rects = [(0,85,1450,800),(190,3,350,35),(460,40,530,40),(908,3,370,35)] #clear out window between clicks
        for rect in clear_rects:
            pygame.draw.rect(screen, 'black', rect)
        #causes less lag if things are only called in their appropriate toggle
        if not rb_ss.toggled:
            all_iterations, all_times = sorting()
            sorting_run()
        else:
            searching_run()

    go_button = util.Button(screen, 1300, 20, 100, 50, 'white ', on_click, "Go")
    buttons = [rb_ss,go_button,rb_ts]


    while running:
        pygame.display.flip()
        for b in buttons:
            b.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for b in buttons:
                    b.handle_mouse_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                for b in buttons:
                    b.handle_mouse_up(event)
            elif event.type == pygame.MOUSEMOTION:
                for b in buttons:
                    b.handle_mouse_motion(event)
            elif event.type == pygame.KEYDOWN:
                for b in buttons:
                    b.handle_key_press(event)

        clock.tick(max_FPS)
        #pygame.display.flip()


if __name__ == '__main__':
    #console_main()
    graphics_main()