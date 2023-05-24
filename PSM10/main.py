import turtle

# Define the L-system parameters
symbols = "XF+-[]"
start_word = "X"
rules = {
    "X": "F+[[X]-X]-F[-FX]+X",
    "F": "FF"
}
angle = 25
iterations = 4

def generate_word(axiom, rules, iterations):
    word = axiom
    for _ in range(iterations):
        new_word = ""
        for symbol in word:
            if symbol in rules:
                new_word += rules[symbol]
            else:
                new_word += symbol
        word = new_word
    return word

def draw_plant(word, angle):
    stack = []
    turtle.speed(0)
    turtle.penup()
    turtle.goto(0, -300)
    turtle.setheading(90)
    turtle.pendown()

    for symbol in word:
        if symbol == "F":
            turtle.forward(5)
        elif symbol == "+":
            turtle.right(angle)
        elif symbol == "-":
            turtle.left(angle)
        elif symbol == "[":
            stack.append((turtle.position(), turtle.heading()))
        elif symbol == "]":
            position, heading = stack.pop()
            turtle.penup()
            turtle.goto(position)
            turtle.setheading(heading)
            turtle.pendown()

    turtle.done()

# Generate the word for the specified number of iterations
final_word = generate_word(start_word, rules, iterations)

# Draw the fractal plant using the generated word
draw_plant(final_word, angle)
