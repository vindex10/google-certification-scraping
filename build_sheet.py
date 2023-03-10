from collections import defaultdict
import sys
import json


def main(fpath):
    with open(fpath, "r", encoding="utf-8") as fin:
        data = load_data(fin)
    course_cache, course_map, norm_roles = parse_roles(data)
    header = ["role"] + [course_map[i]["name"] for i in range(len(course_map))]
    print("\t".join(header))
    for role, course_ids in norm_roles.items():
        course_line = [""] * len(course_cache)
        for course_id in course_ids:
            course = course_map[course_id]
            course_line[course_id] = course["type"]
        res = [role] + course_line
        print("\t".join(res))


def parse_roles(data):
    course_cache = {}
    course_map = {}
    norm_roles = defaultdict(list)
    for role, courses in data.items():
        for course in courses:
            cid = course["url"]
            cid_num = course_cache.setdefault(cid, len(course_cache))
            course_map[cid_num] = course
            norm_roles[role].append(cid_num)
    return course_cache, course_map, norm_roles


def load_data(fin):
    res = {}
    for line in fin:
        one_role = json.loads(line.strip())
        res[one_role["role"]] = one_role["courses"]
    return res


if __name__ == "__main__":
    main(sys.argv[1])
