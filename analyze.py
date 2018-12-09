WEALTH = 1
CONTROL = 0

def _get_index(answer, field):
    ans = answer['choice']['label']
    i = 0
    for f in field['choices']:
        if f['label'] == ans:
            return i
        i += 1
    print("INDEX NOT FOUND")
    import pdb; pdb.set_trace()
    return -1

def wealth_control(answers, fields):
    desire = _get_index(answers[-1], fields[-1])

    info = {}
    answers = answers[:-1]
    fields = fields[:-1]

    inconsistent = []
    ans_desire = []

    for i in range(len(answers)):
        ans = answers[i]
        field = fields[i]
        decision = _get_index(ans, field)

        inconsistent.append(abs(decision - desire))
        ans_desire.append(decision)

    info["answers"] = ans_desire
    info["inconsistent"] = inconsistent
    info["desire"] = desire
    info["wealth"] = WEALTH
    info["control"] = CONTROL

    return info
