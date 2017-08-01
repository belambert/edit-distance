#pylint: skip-file
import timeit

n = 1000

# Sequence pairs to benchmark with
sequences = [(['a', 'b'] * 13, ['a', 'c', 'd', 'a', 'b'] * 5),
             ("'fsffvfdsbbdfvvdavavavavavava'", "'fvdaabavvvvvadvdvavavadfsfsdafvvav'"),
             ([1, 2] * 13, [3, 2, 1, 2, 5] * 5)]

# Functions to test
run_strings = ['edit_distance.edit_distance(a, b)',
               'edit_distance.edit_distance_backpointer(a, b)']
               
for a, b in sequences:
    print('For sequences: a={}, b={}'.format(a, b))
    setup_string = "import edit_distance; a = {}; b = {}".format(a, b)
    for run_string in run_strings:
        print('For: {}'.format(run_string))
        t = timeit.Timer(run_string, setup=setup_string)
        total_time = t.timeit(number=n)
        print('Average time: {:.4} ms'.format(total_time/n * 1000))
