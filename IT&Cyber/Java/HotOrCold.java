package Java;

import java.util.Scanner; 
import java.util.Random;

class HotOrCold {
  public static void main(String[] args) {
    Scanner scanner = new Scanner(System.in);
    Random random = new Random();

    int UpperBound = random.nextInt(0,10000);
    int LowerBound = random.nextInt(0, UpperBound);
    int Answer = random.nextInt(LowerBound, UpperBound);
    int GuessesRemaining = 10;

    System.out.print("Welcome to Hot or Cold!");
    System.out.println(String.format("Guess the number that I am thinking of. Hint: It is between %s and %s", LowerBound, UpperBound));

    while (true) {
        System.out.println("What is your guess?");
        int guess = scanner.nextInt();

        GuessesRemaining -= 1;

        if (guess > Answer) {
            System.out.println("Too Hot!");
            System.out.println(String.format("You have %s guesses left", GuessesRemaining));
        } else if (guess < Answer) {
            System.out.println("Too Cold!");
            System.out.println(String.format("You have %s guesses left", GuessesRemaining));
        } else {
            System.out.println("Correct!");
            System.out.println(String.format("You used %s guesses", 10 - GuessesRemaining));
            break;
        }

        if (GuessesRemaining == 0) {
            System.out.println(String.format("You lost! Answer was %s", Answer));
            break;
        }
    }
    
    scanner.close();
  }
}