import json
import random
import click 
import os
import time 

def load():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_dir, "Uma.json"), "r", encoding="utf-8") as f:
        json_data = json.load(f)
    
    return json_data



def Process(guess: str, result_upper: str) -> None:
    guess_upper = guess.upper()
    
    # Iterate exactly the length of the user's guess
    for i in range(len(guess_upper)):
        # Safely check for an exact match (ensuring i is within bounds of the result)
        if i < len(result_upper) and guess_upper[i] == result_upper[i]:
            click.echo(click.style(guess_upper[i], fg='green', bold=True), nl=False)
            time.sleep(0.1)  # Add a small delay for better user experience
            
        # Character is in the word, but wrong spot (or out of bounds of the actual word length)
        elif guess_upper[i] in result_upper:
            click.echo(click.style(guess_upper[i], fg='yellow', bold=True), nl=False)
            time.sleep(0.1)
            
        # Character is entirely wrong
        else:
            click.echo(click.style(guess_upper[i], fg='red', bold=True), nl=False)
            time.sleep(0.1)
            
    # Add a newline at the end so your terminal prompt doesn't stick to the output
    click.echo()

json_data = load()
result = random.choice(json_data).get("Name", "Unknown Character")
result_upper = result.upper()

@click.command()
def introduction():
    click.echo('-'*50)
    click.secho("Welcome to the Umamusume Guessing Game!", fg='cyan', bold=True)
    click.echo('Use the --guess option to start the game.')
    click.echo() * 3
    click.secho('Hope you enjoy!', fg= 'cyan', bold=True)
    click.echo('-'*50)
    
    
@click.command()
@click.option("--hint", is_flag=True, help="Get a hint about the character.")
@click.option("--guess", prompt="Enter your guess", help="Your guess for the Umamusume character.")
def game(guess: str, hint: bool = False):
     
    if guess.upper() == result_upper:
        
        click.echo()
        click.echo("Congratulations! You guessed the character correctly!")
        Process(guess.upper(), result_upper)
        click.echo()
        click.secho(f'The correct answer was {result}!', bold = True)
        return
    
    else:
        
        click.echo("Wrong guess! Try again.")
        Process(guess.upper(), result_upper)
        
        if hint:
            hint_info = random.choice(json_data)
            click.echo()
            click.secho(f"Here's a hint: {hint_info.get("Slogan", hint_info.get("Profile", "No profile available."))}", fg='blue')
        
        time.sleep(0.5)  # Add a small delay before allowing the next guess
        game()  # Call main again to allow for another guess
        
    

if __name__ == "__main__":
    introduction()
