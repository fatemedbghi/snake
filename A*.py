from heapq import heapify, heappush, heappop 
import time

class Node:
    def __init__(self,state,help_state,cost,parent,action,heuristic):
        self.state = state
        self.help_state = help_state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.heuristic = heuristic
    def __lt__(self, other):
        return self.cost < other.cost

def calc_heuristic(state,h,w,test):
    if test == 0:
        max_ = 0
        for i in state[1]:
            temp1 = abs(min(h-state[0][-1][0],h-i[0])+min(state[0][-1][0],i[0]))
            temp2 = abs(state[0][-1][0]-i[0])
            temp3 = abs(min(w-state[0][-1][1],w-i[1])+min(state[0][-1][1],i[1]))
            temp4 = abs(state[0][-1][1]-i[1])
            max_ = max(max_,min(temp1,temp2)+ min(temp3,temp4))
        return max_
    if test == 1:
        return len(state[1])
    if test == 2:
        return len(state[1])*2
    if test == 3:
        return len(state[1])*10

def Astar(start,h,w,hnumber):
    seen_states = [1,1]
    visited = dict()
    heap = []
    heapify(heap)
    heappush(heap, (start.heuristic + start.cost,start)) 
    
    while True:
        
        node = heappop(heap)[1]
        if node.help_state in visited:
            continue
        visited[node.help_state] = node.cost + node.heuristic

        if node.state[1] == []:
            return node,seen_states

        for i in range(4):
            if i == 0:
                if len(node.state[0]) <= 1 or node.action != 'D':
                    if node.state[0][-1][0] == 0:
                        new = (h-1,node.state[0][-1][1])
                    else:
                        new = (node.state[0][-1][0]-1,node.state[0][-1][1])
                    action = 'U'
                else: continue
            if i == 1:
                if len(node.state[0]) <= 1 or node.action != 'U':
                    if node.state[0][-1][0] == h-1:
                        new = (0,node.state[0][-1][1])
                    else:
                        new = (node.state[0][-1][0]+1,node.state[0][-1][1])
                    action = 'D'
                else: continue
            if i == 2:
                if len(node.state[0]) <= 1 or node.action != 'L':
                    if node.state[0][-1][1] == w-1:
                        new = (node.state[0][-1][0],0)
                    else:
                        new = (node.state[0][-1][0],node.state[0][-1][1]+1)
                    action = 'R'
                else: continue
            if i == 3:
                if len(node.state[0]) <= 1 or node.action != 'R':
                    if node.state[0][-1][1] == 0:
                        new = (node.state[0][-1][0],w-1)
                    else:
                        new = (node.state[0][-1][0],node.state[0][-1][1]-1)
                    action = 'L'
                else: continue


            if new in node.state[0][1:]:
                continue

            new_state = [[],[],False]
            flag_ = 0

            for j in node.state[1]:
                if new == j and flag_ == 0:
                    new_state[2] = True
                    flag_ = 1
                    continue
                new_state[1].append(j)


            for j in node.state[0]:
                new_state[0].append(j)
            if node.state[2] == False:
                new_state[0] = new_state[0][1:]
            new_state[0].append(new)

            h_s = tuple(new_state[0][j] for j in range(len(new_state[0])))
            h_g = tuple(new_state[1][j] for j in range(len(new_state[1])))
            new_help_state = (h_s,h_g,new_state[2])
            he = calc_heuristic(new_state,h,w,hnumber)

            seen_states[0] += 1

            if new_help_state in visited and (he + node.cost+1 < visited[new_help_state]):
                del visited[new_help_state]
            if (new_help_state not in visited):
                new_node = Node(new_state,new_help_state,node.cost+1,node,action,he)
                heappush(heap,(new_node.heuristic + new_node.cost,new_node)) 
                seen_states[1] += 1


def output(node,seen_states,time,test):
    print("distance: ",node.cost)
    print("path:",end=" ")
    f = node
    while f.parent != None:
        print(f.action, end=" ")
        f = f.parent
    print()
    print("seen states: ",seen_states[0])
    print("distinct seen states: ",seen_states[1])
    print("time: ","%.4f" % time)
    print("---------------------------------------------------------")

def get_input(test,hnumber):
    input_ = []
    with open(test) as my_file:
        for line in my_file:
            line = line[:-1]
            input_.append(line)

    goal = []

    for i in range(len(input_)):
        if i == 0:
            h,w = [int(j) for j in input_[i].split(",")]
        elif i == 1:
            t1,t2 = [int(j) for j in input_[i].split(",")]
            initial_state = (t1,t2)
        elif i > 2:
            t1,t2,t3 = [int(j) for j in input_[i].split(",")]
            for i in range(t3):
                goal.append((t1,t2))
    flag = initial_state in goal
    goals = tuple(goal[i] for i in range(len(goal)))
    help_state = ((initial_state),goals,flag)
    h_ = calc_heuristic([[initial_state],goal,flag],h,w,hnumber);
    start = Node([[initial_state],goal,flag],help_state,0,None,None,h_)
    t1 = time.process_time() 
    final_node,seen_states = Astar(start,h,w,hnumber)
    t2 = time.process_time()
    return final_node,seen_states,t2-t1



print('-------------------------test1---------------------------')
print('----> A* <----')
print("admissible heuristic")
print()
node1,seen_states1,time1 = get_input('test1.txt',0)
output(node1,seen_states1,time1,'test1')
print()
print("admissible and consistent heuristic")
print()
node1,seen_states1,time1 = get_input('test1.txt',1)
output(node1,seen_states1,time1,'test1')
print('----> weighted A* <----')
print('‫‪α‬‬ = 2')
print()
node1,seen_states1,time1 = get_input('test1.txt',2)
output(node1,seen_states1,time1,'test1')
print()
print('‫‪α‬‬ = 10')
print()
node1,seen_states1,time1 = get_input('test1.txt',3)
output(node1,seen_states1,time1,'test1')
print('-------------------------test2---------------------------')
print('----> A* <----')
print("admissible heuristic")
print()
node2,seen_states2,time2 = get_input('test2.txt',0)
output(node2,seen_states2,time2,'test2')
print()
print("admissible and consistent heuristic")
print()
node2,seen_states2,time2 = get_input('test2.txt',1)
output(node2,seen_states2,time2,'test2')
print('----> weighted A* <----')
print('‫‪α‬‬ = 2')
print()
node2,seen_states2,time2 = get_input('test2.txt',2)
output(node2,seen_states2,time2,'test2')
print()
print('‫‪α‬‬ = 10')
print()
node2,seen_states2,time2 = get_input('test2.txt',3)
output(node2,seen_states2,time2,'test2')
print('-------------------------test3---------------------------')
print('----> A* <----')
print("admissible heuristic")
print()
node3,seen_states3,time3 = get_input('test3.txt',0)
output(node3,seen_states3,time3,'test3')
print()
print("admissible and consistent heuristic")
print()
node3,seen_states3,time3 = get_input('test3.txt',1)
output(node3,seen_states3,time3,'test3')
print('----> weighted A* <----')
print('‫‪α‬‬ = 2')
print()
node3,seen_states3,time3 = get_input('test3.txt',2)
output(node3,seen_states3,time3,'test3')
print()
print('‫‪α‬‬ = 10')
print()
node3,seen_states3,time3 = get_input('test3.txt',3)
output(node3,seen_states3,time3,'test3')