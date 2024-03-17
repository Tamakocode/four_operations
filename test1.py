def change_to_true(improper_fraction):
    if '/' not in improper_fraction:
        return improper_fraction
    numerator = int(improper_fraction.strip().split('/')[0])
    denominator = int(improper_fraction.strip().split('/')[1])

    whole_part = numerator // denominator
    fraction_part = f"{numerator % denominator}/{denominator}"

    true_fraction = f"{whole_part}'{fraction_part}"
    return true_fraction


# 真变假
def change_to_false(true_fraction):
    if '/' not in true_fraction:
        return true_fraction
    parts = true_fraction.split("'")
    whole_part = int(parts[0])
    fraction_part = parts[1]

    numerator = whole_part * int(fraction_part.split('/')[1]) + int(fraction_part.split('/')[0])
    denominator = int(fraction_part.split('/')[1])

    improper_fraction = f"{numerator}/{denominator}"
    return improper_fraction


print(change_to_true('99/4'))
print(change_to_false('4\'1/3'))
print(change_to_false('77'))
print(change_to_true('66'))
