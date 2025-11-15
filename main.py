

full_lenght = int(input('Podaj całkowitą długość: '))
a_lenght = int(input('Podaj długość sekcji a: '))
a_condition = int(input('Podaj warunek do sekcji a (sama liczba): '))
b_lenght = int(input('Podaj długość sekcji b: '))
b_condition = int(input('Podaj warunek do sekcji b(sama liczba): '))
c_condition = int(input('Podaj warunek do sekcji c(sama liczba): '))

current_section = 0

def checkCondition(current_section,current_condition, next_condition, section_max_lenght):
    if current_condition <  next_condition:
        return current_section < section_max_lenght
    return current_section + current_condition < section_max_lenght

best_division = 5000
best_a_division = 0
best_b_division = 0
best_c_division = 0
best_a_distance = 0
best_b_distance = 0
best_c_distance = 0

a_division = 0
b_division = 0
c_division = 0

for i in range (100):
    for j in range(100):
        a_division = 0
        b_division = 0
        c_division = 0
        current_section = 0
        current_condition = a_condition + i
        next_condition = b_condition + j
        while checkCondition(current_section, current_condition,next_condition, a_lenght):
            current_section += current_condition
            a_division +=1
        while checkCondition(current_section, next_condition,c_condition, a_lenght+b_lenght):
            current_section += next_condition
            b_division+=1

        i = 0
        a = full_lenght -  (current_section *2 )
        b = c_condition
        
        while a%b != 0 and i < 50:
            i+=1
            b-=1
        if a%b == 0:
            c_division = a/b
            if(2*(a_division + b_division) + c_division < best_division):
                best_division = 2*(a_division + b_division) + c_division
                best_a_division = a_division
                best_b_division = b_division
                best_c_division = c_division
                best_a_distance = current_condition
                best_b_distance = next_condition
                best_c_distance = b

print('allDivisions: ', best_division)
print('a_division: ', best_a_division, 'distance: ', best_a_distance)
print('b_division: ', best_b_division, 'distance: ', best_b_distance)
print('c_division: ', best_c_division, 'distance: ', best_c_distance)
