import random

def scream():
    screams=[
        "https://c.tenor.com/m58PfSCzVsMAAAAM/aah-screaming.gif",
        "https://i.imgur.com/dStvIvP.gif",
        "https://media1.giphy.com/media/5lNqZ6xXiyQBwGaCoK/200.gif"
    ]
    return (random.choice(screams))

def cry():
    cries=[
        "https://monophy.com/media/l0DAGrmHDWoVG8i1W/monophy.gif",
        "https://c.tenor.com/do8q_eYrsW4AAAAM/crying-black-guy-meme.gif",
        "https://media0.giphy.com/media/zHd8x7Pik0Ftm/giphy.gif",
        "https://media4.giphy.com/media/L95W4wv8nnb9K/giphy.gif"
    ]
    return (random.choice(cries))