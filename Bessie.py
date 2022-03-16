#!/usr/bin/python

# problem description: http://usaco.org/index.php?page=viewproblem2&cpid=1131

class ProblemAndSolution:
    def __init__(self, N, L, citation_list, expected):
        self.problem = Problem(N, L, citation_list)
        self.expected = expected
    @classmethod
    def from_file(cls, prefix):
        in_file = prefix + '.in'
        with open(in_file) as f:
            parsed_line1 = f.readline().strip().split()
            N = int(parsed_line1[0])
            L = int(parsed_line1[1])
            parsed_line2 = f.readline().strip().split()
            citation_list = list(map(int, parsed_line2))
            f.close()
        out_file = prefix + '.out'
        with open(out_file) as f:
            parsed_line1 = f.readline().strip()
            expected = int(parsed_line1)
            f.close()
        return ProblemAndSolution(N, L, citation_list, expected)
class Problem:
    def __init__(self, N, L, citation_list):
        self.N = N
        self.L = L
        self.citation_list = citation_list
        self.solution = None
    def solve(self):
        if self.solution is None:
            self.solution = self.solve_internal()
        return self.solution
    def solve_internal(self):
        # Given a list and a threshold, it's either possible to increase by 1
        # or not - but it's impossible to increase by more than 1
        (h_index, count, next_count) = self.h_index_fast(self.citation_list)
        if next_count is None:
            return h_index
        target = h_index+1
        have = count - next_count
        need = (h_index+1) - next_count
        if have >= need and self.L >= need:
            return h_index + 1
        else:
            return h_index
    def h_index_fast(self, input_list):
        min_count = self.count_at_threshold(input_list, 1)
        if min_count < 1:
            return (0, len(input_list), 0)
        max_count = self.count_at_threshold(input_list, len(input_list))
        if max_count == len(input_list):
            return (len(input_list), len(input_list), None)
        highest_true = 1
        lowest_false = len(input_list)
        highest_true_count = min_count
        lowest_false_count = max_count
        attempt = 1
        while (lowest_false - highest_true) > 1 and attempt < 100:
            attempt += 1
            guess = highest_true + round((lowest_false - highest_true) / 2)
            guess_count = self.count_at_threshold(input_list, guess)
            if guess_count >= guess:
                highest_true = guess
                highest_true_count = guess_count
            else:
                lowest_false = guess
                lowest_false_count = guess_count
        return (highest_true, highest_true_count, lowest_false_count)
    def h_index_medium(self, input_list):
        # returns (h_index, count, count_at_next_level)
        count_list = []
        next_count = None
        for index in range(0, len(input_list)):
            threshold = index + 1
            count = self.count_at_threshold(input_list, threshold)
            if count < threshold:
                next_count = count
                break
            count_list.append(count)
        # [1, 100, 2, 3] => [4, 3, 2, 1] = [4, 3] => (2, 2)
        # [1, 100, 3, 3] => [4, 3, 3, 1] = [4, 3, 3] => (3, 1)
        # [4, 4, 4, 4] => [4, 4, 4, 4] => (4, None)
        # [0, 0, 0, 0] => [] => (0, 0)
        if len(count_list) == 0:
            return (0, len(input_list), next_count)
        return (len(count_list), count_list[len(count_list)-1], next_count)
    def count_at_threshold(self, input_list, threshold):
        count = sum(map(lambda x : x>=threshold, input_list))
        return count
    def h_index_list(self, input_list):
        # returns a list the same size as input_list, with the ith
        # element (1-indexed!) equal to the number of papers
        # with at least that number of citations
        # h_index_list( [1, 100, 2, 3] ) = [4, 3, 2, 1]
        #   - The h-index is 2
        #   - With 1 citation, can get it to 3
        #   - With 2+ citations, I don't think you can get it higher
        # h_index_list( [1, 100, 3, 3] ) = [4, 3, 3, 1]
        # h_index_list( [1, 100, 4, 4] ) = [4, 3, 3, 1]
        h_index_list = [0] * len(input_list)
        for i in range(len(input_list)):
            citation_count = input_list[i]
            for j in range(0, min(citation_count, len(input_list))):
                h_index_list[j] = h_index_list[j] + 1
        return h_index_list
    def h_index(self, l):
        # returns the h-index for the provided list l
        h_index_list = self.h_index_list(l)
        h_index = 0
        for i in range(len(h_index_list)):
            if h_index_list[i] >= i+1:
                h_index = i+1
            else:
                break
        return h_index
    pass

def test_h_index(name, problem, expected):
    actual = problem.h_index(problem.citation_list)
    result = ('FAIL', 'OK')[int(actual == expected)]
    print('{}: {}'.format(name, result))
def test_h_index_medium(name, problem, expected):
    actual = problem.h_index_medium(problem.citation_list)[0]
    result = ('FAIL', 'OK')[int(actual == expected)]
    print('{}: {}'.format(name, result))
def test_solve(name, problem, expected):
    actual = problem.solve()
    result = ('FAIL', 'OK')[int(actual == expected)]
    print('{}: {}'.format(name, result))
def test_h_index_fast(name, problem, expected):
    actual = problem.h_index_fast(problem.citation_list)[0]
    result = ('FAIL', 'OK')[int(actual == expected)]
    print('{}: {}'.format(name, result))
def test_from_file(prefix):
    problem_and_solution = ProblemAndSolution.from_file(prefix)
    actual = problem_and_solution.problem.solve()
    expected = problem_and_solution.expected
    result = ('FAIL', 'OK')[int(actual == expected)]
    print('{}: {}'.format(prefix, result))

test_h_index("h-index 1", Problem(4, 0, [1, 100, 2, 3]), 2)
test_h_index("h-index 2", Problem(4, 0, [1, 100, 3, 3]), 3)
test_h_index("h-index 3", Problem(1, 0, [1]), 1)
test_h_index_medium("h-index-medium 1", Problem(4, 0, [1, 100, 2, 3]), 2)
test_h_index_medium("h-index-medium 2", Problem(4, 0, [1, 100, 3, 3]), 3)
test_h_index_medium("h-index-medium 3", Problem(1, 0, [1]), 1)
test_solve('solve-1', Problem(4, 1, [1, 100, 2, 3]), 3)
test_solve('solve-2', Problem(4, 0, [1, 100, 2, 3]), 2)
test_solve('solve-3', Problem(1, 0, [0]), 0)
test_solve('solve-4', Problem(1, 1, [0]), 1)
test_solve('solve-5', Problem(1, 1, [1]), 1)
test_solve('solve-6', Problem(4, 1, [4, 4, 4, 4]), 4)
test_h_index_fast('h-index-fast 1', Problem(4, 0, [1, 100, 2, 3]), 2)
test_h_index_fast('h-index-fast 2', Problem(4, 0, [1, 100, 3, 3]), 3)
test_h_index_fast("h-index-fast 3", Problem(1, 0, [1]), 1)
test_solve('solve-1', Problem(4, 1, [1, 100, 2, 3]), 3)
test_solve('solve-2', Problem(4, 0, [1, 100, 2, 3]), 2)
test_solve('solve-3', Problem(1, 0, [0]), 0)
test_solve('solve-4', Problem(1, 1, [0]), 1)
test_solve('solve-5', Problem(1, 1, [1]), 1)
test_solve('solve-6', Problem(4, 1, [4, 4, 4, 4]), 4)
test_from_file('1')
test_from_file('2')
test_from_file('3')
test_from_file('4')
test_from_file('5')
test_from_file('6')
test_from_file('7')
test_from_file('8')
test_from_file('9')
test_from_file('10')
test_from_file('11')
test_from_file('12')
test_from_file('13')
test_from_file('14')
test_from_file('15')
test_from_file('16')
test_from_file('17')
