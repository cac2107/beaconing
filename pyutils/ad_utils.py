import pyad
from platform import python_compiler

def get_users():
    python_compiler.CoInitialize()
    query = pyad.adquery.ADQuery()
    query.execute_query(attributes=["sAMAccountName", "displayName", "memberOf"], where_clause="objectClass='user'")

    finalstr = ""
    for user in query.get_results():
        username = user["sAMAccountName"]
        fullname = user["displayName"]
        groups = user.get("memberOf", [])

        if not isinstance(groups, list):
            groups = [groups]

        groups = [str(group) for group in groups if group is not None]
        groupstr = ""
        for group in groups:
            split = group.split(",")
            sstr = "\n"
            for s in split:
                if s.startswith("DC") is False:
                    color = "\t\033[31;1m"
                    if s.startswith("OU"): color = "\033[34;1m"
                    s = s.strip().replace('(', '').replace("'", '')
                    sstr += f"{color}{s}\t\033[0m"

            groupstr += sstr + "\n"

        finalstr += f"Username: {username}\nFull Name: {fullname}\nGroups:\n{groupstr}\n-------------\n"

    with open("test.txt", 'w') as f:
        f.write(finalstr)
    return finalstr
