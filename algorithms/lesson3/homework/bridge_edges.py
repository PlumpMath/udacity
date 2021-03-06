import pdb
import operator

# Bridge Edges v4
#
# Find the bridge edges in a graph given the
# algorithm in lecture.
# Complete the intermediate steps
#  - create_rooted_spanning_tree
#  - post_order
#  - number_of_descendants
#  - lowest_post_order
#  - highest_post_order
#
# And then combine them together in
# `bridge_edges`

# So far, we've represented graphs
# as a dictionary where G[n1][n2] == 1
# meant there was an edge between n1 and n2
#
# In order to represent a spanning tree
# we need to create two classes of edges
# we'll refer to them as "green" and "red"
# for the green and red edges as specified in lecture
#
# So, for example, the graph given in lecture
# G = {'a': {'c': 1, 'b': 1},
#      'b': {'a': 1, 'd': 1},
#      'c': {'a': 1, 'd': 1},
#      'd': {'c': 1, 'b': 1, 'e': 1},
#      'e': {'d': 1, 'g': 1, 'f': 1},
#      'f': {'e': 1, 'g': 1},
#      'g': {'e': 1, 'f': 1}
#      }
# would be written as a spanning tree
# S = {'a': {'c': 'green', 'b': 'green'},
#      'b': {'a': 'green', 'd': 'red'},
#      'c': {'a': 'green', 'd': 'green'},
#      'd': {'c': 'green', 'b': 'red', 'e': 'green'},
#      'e': {'d': 'green', 'g': 'green', 'f': 'green'},
#      'f': {'e': 'green', 'g': 'red'},
#      'g': {'e': 'green', 'f': 'red'}
#      }

def combine_dicts(a, b, op=operator.add):
    return dict(a.items() + b.items() +
        [(k, op(a[k], b[k])) for k in set(b) & set(a)])

def make_tree_link(G, node1, node2, color):
    print "making a %s link between %s and %s:" % (color, node1, node2)
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = color
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = color
    return G

def postorder_traverse(G, node, marked, node_func):
     marked[node] = True
     for neighbor in G[node]:
         if neighbor not in marked:
             postorder_traverse(G, neighbor, marked, node_func)
             node_func(node, neighbor)
#
# def find_green_dfs(G, T, node, marked):
#     marked[node] = True
#     print "find_green:", node
#
#     for neighbor in G[node]:
#         if neighbor not in marked:
#             make_tree_link(T, node, neighbor, "green")
#             find_green(G, T, neighbor, marked)

def bfs(G, T, node, marked, node_func):
    marked[node] = True
    todo = [node]

    while len(todo) > 0:
        current = todo[0]
        del todo[0]
        for neighbor in G[current]:
            if neighbor not in marked:
                marked[neighbor] = True
                node_func(current, neighbor)
                # make_tree_link(T, current, neighbor, "green")
                todo.append(neighbor)
            else:
                print "already marked neighbor:", neighbor
    return T


#BFS approach
def find_green(G, T, root, marked):
    node_func = lambda current, neighbor: make_tree_link(T, current, neighbor, "green")
    return bfs(G, T, root, marked, node_func)

def find_red_from_green(G, T, greens, root, marked):
    def node_func(current, neighbor):
        if current in greens and neighbor in greens[current]:
            # greens[current][neighbor]:
            #print "This link already exists: (%s, %s)" % (current, neighbor)
            pass
        else:
            #print "Making a RED link: (%s, %s)" % (current, neighbor)
            make_tree_link(T, current, neighbor, "red")
    #return bfs(G, T, root, marked, node_func)
    return postorder_traverse(G, root, marked, node_func)

def create_rooted_spanning_tree(G, root):
    green = find_green(G, {}, root, {})

    reds = {}
    find_red_from_green(G, reds, green, root, {})

    total = combine_dicts(green, reds, op=combine_dicts)

    #postorder_traverse(G, S, root, {}
    # first, perform a DFS to establish all of the green edges

    # second, perform a traversal of our tree to add the red edges

    return total

# This is just one possible solution
# There are other ways to create a
# spanning tree, and the grader will
# accept any valid result
# feel free to edit the test to
# match the solution your program produces
def test_create_rooted_spanning_tree():
    G = {'a': {'c': 1, 'b': 1},
         'b': {'a': 1, 'd': 1},
         'c': {'a': 1, 'd': 1},
         'd': {'c': 1, 'b': 1, 'e': 1},
         'e': {'d': 1, 'g': 1, 'f': 1},
         'f': {'e': 1, 'g': 1},
         'g': {'e': 1, 'f': 1}
         }
    S = create_rooted_spanning_tree(G, "a")
    assert S == {'a': {'c': 'green', 'b': 'green'},
                 'b': {'a': 'green', 'd': 'red'},
                 'c': {'a': 'green', 'd': 'green'},
                 'd': {'c': 'green', 'b': 'red', 'e': 'green'},
                 'e': {'d': 'green', 'g': 'green', 'f': 'green'},
                 'f': {'e': 'green', 'g': 'red'},
                 'g': {'e': 'green', 'f': 'red'}
                 }, "Spanning tree: %s" % S

###########

def post_traverse(G, node, marked, mapping, current_value):
    # print "TRAVERSING node: %s" % node
    marked[node] = 1
    for neighbor in reversed(list(G[node])):
        color = G[node][neighbor]
        if neighbor not in marked:
            if color == 'green':
                new_value = post_traverse(G, neighbor, marked, mapping, current_value)
                marked[neighbor] = 1
                current_value = new_value
            else:
                pass
                #print "neighbor was red:", neighbor
        else:
            pass
            #print "neighbor was already marked:", neighbor

    mapping[node] = current_value

    return current_value + 1


def post_order(S, root):
    # return mapping between nodes of S and the post-order value
    # of that node
    mapping = {}
    post_traverse(S, root, {}, mapping, 1)
    return mapping

# This is just one possible solution
# There are other ways to create a
# spanning tree, and the grader will
# accept any valid result.
# feel free to edit the test to
# match the solution your program produces
def test_post_order():
    S = {'a': {'c': 'green', 'b': 'green'},
         'b': {'a': 'green', 'd': 'red'},
         'c': {'a': 'green', 'd': 'green'},
         'd': {'c': 'green', 'b': 'red', 'e': 'green'},
         'e': {'d': 'green', 'g': 'green', 'f': 'green'},
         'f': {'e': 'green', 'g': 'red'},
         'g': {'e': 'green', 'f': 'red'}
         }
    po = post_order(S, 'a')
    assert po == {'a':7, 'b':1, 'c':6, 'd':5, 'e':4, 'f':2, 'g':3}, "po was: %s" % po

##############

def descendants_recur(G, node, marked, descendants):
    marked[node] = True
    num_descendants = 1

    for child in G[node]:
        color = G[node][child]
        if child not in marked and color == 'green':
            child_descendants = descendants_recur(G, child, marked, descendants)
            num_descendants += child_descendants

    descendants[node] = num_descendants

    return num_descendants


def number_of_descendants(S, root):
    # return mapping between nodes of S and the number of descendants
    # of that node
    descendants = {}
    descendants_recur(S, root, {}, descendants)
    return descendants

def test_number_of_descendants():
    S =  {'a': {'c': 'green', 'b': 'green'},
          'b': {'a': 'green', 'd': 'red'},
          'c': {'a': 'green', 'd': 'green'},
          'd': {'c': 'green', 'b': 'red', 'e': 'green'},
          'e': {'d': 'green', 'g': 'green', 'f': 'green'},
          'f': {'e': 'green', 'g': 'red'},
          'g': {'e': 'green', 'f': 'red'}
          }
    nd = number_of_descendants(S, 'a')
    assert nd == {'a':7, 'b':1, 'c':5, 'd':4, 'e':3, 'f':1, 'g':1}, "ND: %s" % nd

###############

def dfs_lowest(G, node, po, marked, mapping, reds_used):
    lowest_postorder = po[node]
    marked[node] = True
    # is this ok? Seems fishy.
    reds_used = 0

    for neighbor in reversed(list(G[node])):
        if neighbor not in marked:
            color = G[node][neighbor]
            if color == 'green':
                value = dfs_lowest(G, neighbor, po, marked, mapping, reds_used)
                lowest_postorder = min(value, lowest_postorder)
            elif color == 'red' and reds_used < 1:
                # print "USING A RED:", neighbor
                reds_used += 1
                value = dfs_lowest(G, neighbor, po, marked, mapping, reds_used)
                lowest_postorder = min(value, lowest_postorder)
            else:
                print "neighbor not valid to traverse:", neighbor

    mapping[node] = lowest_postorder

    return lowest_postorder

def dfs_highest(G, node, po, marked, mapping, reds_used):
    print "Traversing node:", node
    highest_postorder = po[node]
    marked[node] = True
    # is this ok? Seems fishy.
    reds_used = 0

    for neighbor in reversed(list(G[node])):
        if neighbor not in marked:
            color = G[node][neighbor]
            if color == 'green':
                value = dfs_highest(G, neighbor, po, marked, mapping, reds_used)
                highest_postorder = max(value, highest_postorder)
            elif color == 'red' and reds_used < 1:
                print "USING A RED:", neighbor
                reds_used += 1
                value = dfs_highest(G, neighbor, po, marked, mapping, reds_used)
                highest_postorder = max(value, highest_postorder)
            else:
                print "neighbor not valid to traverse:", neighbor

    mapping[node] = highest_postorder
    print "Highest for node: %s was: %s" % (node, highest_postorder)

    return highest_postorder

def lowest_post_order(S, root, po):
    # return a mapping of the nodes in S
    # to the lowest post order value
    # below that node
    # (and you're allowed to follow 1 red edge)
    mapping = {}
    result = dfs_lowest(S, root, po, {}, mapping, 0)
    return mapping

def test_lowest_post_order():
    S = {'a': {'c': 'green', 'b': 'green'},
         'b': {'a': 'green', 'd': 'red'},
         'c': {'a': 'green', 'd': 'green'},
         'd': {'c': 'green', 'b': 'red', 'e': 'green'},
         'e': {'d': 'green', 'g': 'green', 'f': 'green'},
         'f': {'e': 'green', 'g': 'red'},
         'g': {'e': 'green', 'f': 'red'}
         }
    po = post_order(S, 'a')
    l = lowest_post_order(S, 'a', po)
    assert l == {'a':1, 'b':1, 'c':1, 'd':1, 'e':2, 'f':2, 'g':2}, "lowest: %s" % l


################

def highest_post_order(S, root, po):
    # return a mapping of the nodes in S
    # to the highest post order value
    # below that node
    # (and you're allowed to follow 1 red edge)
    mapping = {}
    result = dfs_highest(S, root, po, {}, mapping, 0)
    return mapping

def test_highest_post_order():
    S = {'a': {'c': 'green', 'b': 'green'},
         'b': {'a': 'green', 'd': 'red'},
         'c': {'a': 'green', 'd': 'green'},
         'd': {'c': 'green', 'b': 'red', 'e': 'green'},
         'e': {'d': 'green', 'g': 'green', 'f': 'green'},
         'f': {'e': 'green', 'g': 'red'},
         'g': {'e': 'green', 'f': 'red'}
         }
    po = post_order(S, 'a')
    h = highest_post_order(S, 'a', po)
    assert h == {'a':7, 'b':5, 'c':6, 'd':5, 'e':4, 'f':3, 'g':3}, "highest: %s" % h

#################

def bridge_edges(G, root):
    # use the four functions above
    # and then determine which edges in G are bridge edges
    # return them as a list of tuples ie: [(n1, n2), (n4, n5)]
    pass

def test_bridge_edges():
    G = {'a': {'c': 1, 'b': 1},
         'b': {'a': 1, 'd': 1},
         'c': {'a': 1, 'd': 1},
         'd': {'c': 1, 'b': 1, 'e': 1},
         'e': {'d': 1, 'g': 1, 'f': 1},
         'f': {'e': 1, 'g': 1},
         'g': {'e': 1, 'f': 1}
         }
    bridges = bridge_edges(G, 'a')
    assert bridges == [('d', 'e')]

# test_bridge_edges()
test_create_rooted_spanning_tree()
#test_highest_post_order()
test_lowest_post_order()
test_number_of_descendants()
test_post_order()
