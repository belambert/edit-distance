"""
py-editdistance
=====

Python implementation of Levenshtein edit distance

Based in part off the Wikipedia code samples at
http://en.wikipedia.org/wiki/Levenshtein_distance.

Usage
-----

...

"""
__author__ = 'Benjamin Lambert'
__version__ = (0, 1, 0)
__license__ = 'tbd'

import operator




def lowest_cost_action(ic, dc, sc, im, dm, sm, cost):
     best_action = None
     best_match_count = -1
     min_cost = min(ic, dc, sc)
     if min_cost == sc and cost == 0:
          best_action = 'equal'
          best_match_count = sm
     if min_cost == sc and cost == 1:
          best_action = 'replace'
          best_match_count = sm
     if min_cost == ic and im > best_match_count:
          best_action = 'insert'
          best_match_count = im
     if min_cost == dc and dm > best_match_count:
          best_action = 'delete'
          best_match_count = dm
     return best_action

def highest_match_action(ic, dc, sc, im, dm, sm, cost):
     best_action = None
     lowest_cost = float("inf")
     max_match = max(im, dm, sm)     
     if max_match == sm and cost == 0:
          best_action = 'equal'
          lowest_cost = sm
     if max_match == sm and cost == 1:
          best_action = 'replace'
          lowest_cost = sm
     if max_match == im and ic < lowest_cost:
          best_action = 'insert'
          lowest_cost = ic
     if max_match == dm and dc < lowest_cost:
          best_action = 'delete'
          lowest_cost = dc
     return best_action     



class SequenceMatcher:
    """Similar to the difflib SequenceMatcher, but uses Levenshtein/edit distance."""

    def __init__(self, a, b, test=operator.eq, action_function=lowest_cost_action):
         self.seq1 = a
         self.seq2 = b
         self.reset_object()
         self.action_function = action_function
         
    def set_seqs(self, a, b):
        set_seq1(a)
        set_seq2(b)

    def reset_object(self):
        self.opcodes = None
        self.dist = None
        self._matches_ = None

    def set_seq1(self, a):
        reset_object()
        self.seq1 = a

    def set_seq2(self, b):
        reset_object()
        self.seq2 = b

    def find_longest_match(self, alo, ahi, blo, bhi):
        pass

    def get_matching_blocks(self):
        opcodes = self.get_opcodes()
        match_opcodes = filter(lambda x: x[0] == 'equal', opcodes)
        return map (lambda opcode: [opcode[1], opcode[3], opcode[2] - opcode[1]], match_opcodes)

    def get_opcodes(self):
        if not self.opcodes:
             self.dist, self.opcodes = edit_distance_backpointer(self.seq1, self.seq2, action_function=self.action_function)
        return self.opcodes

    def get_grouped_opcodes(self, n=None):
        pass

    def ratio(self):
        return 2.0* self.matches()/ (len(self.seq1) + len(self.seq2))

    def quick_ratio(self):
        return self.ratio()

    def real_quick_ratio(self):
        return self.ratio()

    def distance(self):
        if not self.dist:
            self.dist, self._matches_ = edit_distance(self.seq1, self.seq2, action_function=self.action_function)
        return self.dist

    def matches(self):
        if not self._matches_:
             self.dist, self._matches_ = edit_distance(self.seq1, self.seq2)
        return self._matches_



def edit_distance(seq1, seq2, action_function=lowest_cost_action):
    matches = 0
    errors = 0
    m = len(seq1)
    n = len(seq2)
    # Special, easy cases:
    if seq1 == seq2:
        return 0, n
    if m == 0:
        return n, 0
    if n == 0:
        return m, 0
   # The two 'error' columns
    v0 = [0]* (n+1)
    v1 = [0]* (n+1)
    # The two 'match' columns
    m0 = [0]* (n+1)
    m1 = [0]* (n+1)        
    for i in xrange(1, n+1):
        v0[i] = i
    for i in xrange(1, m+1):
        v1[0] = i + 1;
        for j in xrange(1, n+1):
            cost = 0 if seq1[i-1] == seq2[j-1] else 1
            # The costs
            ins_cost = v1[j-1] + 1
            del_cost = v0[j] + 1
            sub_cost = v0[j-1] + cost
            # Match counts
            ins_match = m1[j-1]
            del_match = m0[j]
            sub_match = m0[j-1] + int (not cost)
                        
            action = action_function(ins_cost, del_cost, sub_cost, ins_match, del_match, sub_match, cost)

            if action == 'equal' or action == 'replace':
                 v1[j] = sub_cost
                 m1[j] = sub_match
            elif action == 'insert':
                 v1[j] = ins_cost
                 m1[j] = ins_match
            elif action == 'delete':
                 v1[j] = del_cost
                 m1[j] = del_match
            else:
                 raise Exception('Invalid dynamic programming option returned!')                 
        # Copy the columns over
        for i in xrange(0, n+1):
            v0[i] = v1[i]
            m0[i] = m1[i]
    return v1[n], m1[n]


def edit_distance_backpointer(seq1, seq2, action_function=lowest_cost_action):
     matches = 0
     errors = 0
     # Create a 2d distance array
     m = len(seq1)
     n = len(seq2)
     # distances array:
     d = [[0 for x in range(n+1)] for y in range(m+1)]
     # backpointer array:
     bp = [[None for x in range(n+1)] for y in range(m+1)]
     # matches array:
     matches = [[0 for x in range(n+1)] for y in range(m+1)]
     # source prefixes can be transformed into empty string by dropping all characters
     for i in xrange(1, m+1):
          d[i][0] = i
          bp[i][0] = ['delete', i-1, i, 0, 0]
     # target prefixes can be reached from empty source prefix by inserting every characters
     for j in xrange(1, n+1):
          d[0][j] = j
          bp[0][j] = ['insert', 0, 0, j-1, j]
     # compute the edit distance...
     for i in xrange(1, m+1):
          for j in xrange(1, n+1):

               cost = 0 if seq1[i-1] == seq2[j-1] else 1
               # The costs of each action...
               ins_cost =  d[i][j-1] + 1   # insertion
               del_cost =  d[i-1][j] + 1   # deletion
               sub_cost = d[i-1][j-1] + cost # substitution/match

               # The match scores of each action
               ins_match = matches[i][j-1]
               del_match = matches[i-1][j]
               sub_match = matches[i-1][j-1] + int (not cost)
               
               action = action_function(ins_cost, del_cost, sub_cost, ins_match, del_match, sub_match, cost)

               if action == 'equal':
                    d[i][j] = sub_cost
                    matches[i][j] = sub_match
                    bp[i][j] = ['equal', i-1, i, j-1, j]                    
               elif action == 'replace':
                    d[i][j] = sub_cost
                    matches[i][j] = sub_match
                    bp[i][j] = ['replace', i-1, i, j-1, j]
               elif action == 'insert':
                    d[i][j] = ins_cost
                    matches[i][j] = ins_match
                    bp[i][j] = ['insert', i-1, i-1, j-1, j]
               elif action == 'delete':
                    d[i][j] = del_cost
                    matches[i][j] = del_match
                    bp[i][j] = ['delete', i-1, i, j-1, j-1]
               else:
                    raise Exception('Invalid dynamic programming action returned!')                 

     opcodes = get_opcodes_from_bp_table(bp)
     return d[m][n], opcodes

def get_opcodes_from_bp_table(bp):
     x = len(bp) - 1
     y = len(bp[0]) - 1
     opcodes = []
     while x != 0 or y != 0:
          this_bp = bp[x][y]
          opcodes.append(this_bp)
          if this_bp[0] == 'equal' or this_bp[0] == 'replace':
               x = x - 1
               y = y - 1
          elif this_bp[0] == 'insert':
               y = y - 1
          elif this_bp[0] == 'delete':
               x = x - 1
     opcodes.reverse()
     return opcodes
    
def main():

    # Should be 3, 2
    a = ['a', 'b']
    b = ['a', 'c', 'd', 'a', 'b']

    print edit_distance_backpointer(a, b)
    print edit_distance(a, b)

    # Should be 4, 2
    a = ['hi', 'my', 'name', 'is', 'andy']
    b = ['hi', "i'm", 'my', "name's", 'sandy']

    print edit_distance_backpointer(a, b)
    print edit_distance(a, b)

    # Should be 5, 0
    # Or        6, 1    
    a = ['are', 'you', 'at', 'work', 'now']
    b = ['i', 'feel', 'are', 'saying']

    print edit_distance_backpointer(a, b)
    print edit_distance(a, b)
    

if __name__ == "__main__":
    main()
