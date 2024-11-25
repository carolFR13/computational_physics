import random
'''
code to solve Monty Hall problem
'''

def box_prob(): 
    '''
    returns a box configuration
    '''
    rd = random.random()
    if rd <= (1/3):
        box = [1,0,0]
    elif rd <= (2/3):
        box = [0,1,0]
    else:
        box = [0,0,1]
    return box


rd = random.random()

count1 = 0 ; count2 = 0 ; total_count_1 = 0 ; total_count_2 = 0

for i in range(10000):
    
    config = box_prob()
    choice1 = config[0] # the player chooses a box, the first one
    presenter_choice = config[1:] #two boxes remaining for the presenter
    presenter_choice.remove(0) # presenter removes the box without the ball

    rd = random.random()

    if rd <= 0.5:
        choice2 = choice1
        total_count_1 +=1
        if choice2 == 1:
            count1 += 1
    else:
        choice2 = presenter_choice[0]
        total_count_2 +=1
        if choice2 == 1:
            count2 +=1

print('Sen cambiar a caixa o espectador adiviña a correcta', count1, 'de', total_count_1, 'veces', (count1/total_count_1)*100,'%')
print('Cambiando a caixa o espectador adiviña a correcta', count2, 'de', total_count_2, 'veces', (count2/total_count_2)*100,'%')
    





