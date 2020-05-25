import random
import operator
import sys


# Function is used to generate a list consisting of the sum, equation, first and second number.
# Selecting the 'Random Sums(5)' option prompts a recursive call to randomly choose another statement.
def equation(selection, x, y):
    if selection == 1:
        return [(x + y), (x, '+', y)]
    elif selection == 2:
        return [(x - y), (x, '-', y)]
    elif selection == 3:
        return [(x * y), (x, '×', y)]
    elif selection == 4:
        return [(x / y), (x, '÷', y)]
    elif selection == 5:
        return equation(random.randint(1, 4), x, y)


# Function generates a positive integer; assigns of two the first and second number random values within
# set range, calculates the answer and evaluates it to prevent decimals number or negative integers.
def positiveInteger(level):
    x = random.randint(1, level)
    y = random.randint(1, level)
    answer = equation(selection, x, y)
    while float(answer[0]) % 1 != 0 or float(answer[0]) < 0:
        answer = positiveInteger(level)
    return answer


# Function allows the user to go through the step by step working out of an answer; done by iterating through a for
# loop and incrementing the values as the step increases, once the for loop has finished, all steps have been displayed.
def helpEnabled(equationBody, isEnabled):
    if isEnabled == "Y" or isEnabled == "y":
        print("Press 'Enter' to Walk-through the Steps:")
        count = 1
        ops = {"+": operator.add, "-": operator.sub, "÷": operator.truediv, "×": operator.mul}
        for x in range(0, equationBody[1][2]):
            total = ops[str(equationBody[1][1])](equationBody[1][0], count)
            input(' '.join(map(str, (["Step", count, ": ", equationBody[1][0], equationBody[1][1], count, "=", total]))))
            count += 1


# Function is used to mark the user's text file; reads the inputted equation and compares the user's
# answer with the system's evaluated answer.
def readSubmission():
    filePath = 'Submission.txt'
    with open(filePath) as fp:
        next(fp)
        counter = 1
        correct = 0
        for line in fp:
            equationBody = (line.strip("\n").split("="))
            if eval(equationBody[0]) == int(equationBody[1]):
                result = "Correct"
                correct += 1
            else:
                result = "Wrong"
            print("Question ", counter, ': ', equationBody[0], "=", equationBody[1], "\t\t", result, "\t| Correct Answer is ", int(eval(equationBody[0])),sep="")
            counter += 1
    print("\nYou got", int((correct*100)/(counter-1)), "Percent Correct.\n")


# Function generates a listing of the user's scores in the different selection categories and suggests
# areas for the user's improvement based on the lowest scores.
def viewScores(scoreList):
    lowestScoreHolder = ""
    lowestScore = min(scoreList)
    for selection, score in enumerate(scoreList[1:], 1):
        print('Selection {}: {}'.format(selection, score))
        if scoreList[selection] <= lowestScore:
            lowestScoreHolder += (str(selection) + ", ")
    print("\nIt Seems You Need to Work on Some Areas, I Suggest the following Selection Categories:", lowestScoreHolder, end="\n\n")
    return lowestScoreHolder


# Function is used to control the level (difficulty range) and print out the level that the user is currently on.
# Only called if correct or wrong is equivalent to 3 and the level is in the allowed range as viewed in the main.
def levelControl(level, correct):
    if correct == 3:
        level += 1
    else:
        level -= 1
    print('\033[1m{}{}{}\033[0m'.format("\nYou're now on level ", level, ", Continue?"))
    return level


# Function is used to invoke while loop where user answer's questions based on their selected menuOption, the behaviour
# of start game is also influenced by the help-mode function which would optionally break-down the user's answer.
def startGame(level, gameState, isEnabled):
    correct = wrong = 0
    while gameState == "Y" or gameState == "y":
        try:
            answer = positiveInteger(level)
            print("\n---------------------------------------------------------------------\nWhat is", *answer[1])
            guess = int(input())
            helpEnabled(answer, isEnabled)
            if guess == int(answer[0]):
                scores[selection] += 1
                correct += 1
                wrong = 0
                print("That is correct, well done! Press Y to try another sum or N to stop.")
            else:
                scores[selection] -= 1
                correct = 0
                wrong += 1
                print("Not right, the correct answer is: ", answer[0], ", Press Y to try another sum or N to stop.")
            if (correct == 3 and level < 10) or (wrong == 3 and level > 4):
                level = levelControl(level, correct)
                correct = wrong = 0
            gameState = input()
        except ValueError:
            print("Please enter a number")


# Main Program Variables:
menuOptions = [1, 2, 3, 4, 5, 6, 7, 8]  # Each Element represents an arithmetic mode in the game, '6' quits game
scores = [0, 0, 0, 0, 0, 0]             # Scores is a list used to hold the user's score in each category
selection = 0                           # Selection assigned value of 0 until the selects a choice from the menuOptions

# Main Program Method (Presents user with different arithmetic options, selected option is used to start the game)
while True:
        try:
            print("Select one of the following options:")
            print("(1) Addition", "(2) Subtraction", "(3) Multiplication", "(4) Division", "(5) Random Sums", "(6) Quit", "(7) View Scores", "(8) Mark Submission")
            selection = int(input())
            if selection == 1:
                print("\nYou have selected Addition\n")
            elif selection == 2:
                print("\nYou have selected Subtraction\n")
            elif selection == 3:
                print("\nYou have selected Multiplication\n")
            elif selection == 4:
                print("\nYou have selected Division\n")
            elif selection == 5:
                print("\nYou have selected Random Sums\n")
            elif selection == 6:
                print("You have Quit the application\n")
                sys.exit(0)
            elif selection == 7:
                viewScores(scores)
            elif selection == 8:
                readSubmission()
            if selection in menuOptions and selection != 7 and selection != 8:
                print("For Help (Walk-through Mode), Press 'Y'")
                mode = input()
                startGame(4, "Y", mode)
        except ValueError:
            print("Please Enter a Number That Matches the Stated Options (1-7).\n")