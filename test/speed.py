# Copyright 2013-2020 Ben Lambert

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import timeit

n = 1000

# Sequence pairs to benchmark with
sequences = [(['a', 'b'] * 13, ['a', 'c', 'd', 'a', 'b'] * 5),
             ("'fsffvfdsbbdfvvdavavavavavava'",
              "'fvdaabavvvvvadvdvavavadfsfsdafvvav'"),
             ([1, 2] * 13, [3, 2, 1, 2, 5] * 5)]

# Functions to test
run_strings = ['edit_distance.edit_distance(a, b)',
               'edit_distance.edit_distance_backpointer(a, b)']


def speed_tests():
    for a, b in sequences:
        print('For sequences: a={}, b={}'.format(a, b))
        setup_string = "import edit_distance; a = {}; b = {}".format(a, b)
        for run_string in run_strings:
            print('For: {}'.format(run_string))
            t = timeit.Timer(run_string, setup=setup_string)
            total_time = t.timeit(number=n)
            print('Average time: {:.4} ms'.format(total_time/n * 1000))
