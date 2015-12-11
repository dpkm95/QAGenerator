import input_parser
import json
from db_helper import *
import qgen
import grammar_helper as gh

def get_qam_string(qam):
    return "Q. " + qam[0] + "\nA. " + qam[1] +"\nMarks: " + str(qam[2])


def get_all_qam_string(ql):
    return "\n".join([get_qam_string(i) for i in ql])

if __name__ == "__main__":
    answer_set = []
    new_sets = []
    while True:
        line = input()
        if line == "end": break
        base = json.loads(line)
        input_parser.insert_into_db(base)

        new_set = []
        for i in [i for i in DbHelper.entities if not (is_class(i) and gh.is_proper_noun(i))]:
            for j in qgen.gen_all_questions(i):
                if tuple(j) not in answer_set:
                    answer_set.append(tuple(j))
                    new_set.append(tuple(j))
        new_sets.append(get_all_qam_string(new_set))

    print(json.dumps(new_sets))


