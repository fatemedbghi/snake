import time
class Node:
    def __init__(self,state,help_state,cost,parent,action):
        self.state = state
        self.help_state = help_state
        self.parent = parent
        self.action = action
        self.cost = cost
    
def BFS(start,h,w):
    seen_states = [1,1]
    visited = set()
    queue = [] 
    queue.append(start) 
    visited.add(start.help_state)
    while True: 
        node = queue.pop(0)
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

            seen_states[0] += 1

            if (new_help_state not in visited):
                new_node = Node(new_state,new_help_state,node.cost+1,node,action)
                queue.append(new_node)
                visited.add(new_node.help_state)
                seen_states[1] += 1
                if new_node.state[1] == []:
                    return new_node,seen_states

def output(node,seen_states,time,test):
    print(test)
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

def get_input(test):
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
    start = Node([[initial_state],goal,flag],help_state,0,None,None)
    t1 = time.process_time() 
    final_node,seen_states = BFS(start,h,w)
    t2 = time.process_time()
    return final_node,seen_states,t2-t1


print("----> BFS <----")
node1,seen_states1,time1 = get_input('test1.txt')
output(node1,seen_states1,time1,'test1')
node2,seen_states2,time2 = get_input('test2.txt')
output(node2,seen_states2,time2,'test2')
node3,seen_states3,time3 = get_input('test3.txt')
output(node3,seen_states3,time3,'test3')