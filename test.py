commentary = "Asistha Fernanda to Axar Patel, no runoff-stump yorker"
tokens = commentary.split(",")[0].split(" to ")
if len(tokens) == 2:
    bowler = tokens[0].strip()
    batsman = tokens[1].strip()
    print(bowler)
    print(batsman)