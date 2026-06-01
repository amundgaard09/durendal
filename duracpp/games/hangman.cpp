
#include <unordered_map>
#include <iostream>
#include <string>
#include <vector>

int _int_clip(int value, int upper, int lower) {
    if (value > upper) { return upper; } 
    else if (value < lower) { return lower; } 
    else { return value; }
}

int main() {
    
    int Difficulty;
    int GuessCount = 0;
    int IncorrectGuessCount = 0;
    bool GameComplete = false;
    char GuessedLetter;

    std::string GuessedWord;
    std::string ActualWord;
    std::unordered_map<int, std::vector<std::string>> WordDatabase = {
        {3, {"cat", "dog", "sun", "hat", "run", "big", "cup"}},
        {4, {"tree", "frog", "jump", "wind", "fire", "lamp", "duck"}},
        {5, {"apple", "brick", "cloud", "flame", "grape", "piano", "stone"}},
        {6, {"bridge", "candle", "flight", "jungle", "mirror", "rocket", "castle"}},
        {7, {"battery", "blanket", "captain", "dolphin", "emperor", "fantasy", "lantern"}},
        {8, {"aircraft", "backpack", "calendar", "dinosaur", "elephant", "firework", "goldfish"}},
        {9, {"adventure", "bookshelf", "chocolate", "dandelion", "evergreen", "flagstone", "grassland"}},
        {10,{"strawberry", "accomplish", "birthplace", "changeable", "discretion", "earthquake", "floorboard"}}
    };

    std::cout << "Welcome to Hangman!" << std::endl;
    std::cout << "Select the Word Length (3 - 10): " << std::endl;
    std::cin >> Difficulty;

    Difficulty = _int_clip(Difficulty, 10, 3);

    std::string GuessedLetters;
    std::vector<std::string>& WordList = WordDatabase[Difficulty];
    ActualWord = WordList[rand() % WordList.size()];
    std::string GuessWord(ActualWord.length(), '_');

    while (!GameComplete) {
        std::cout << "Input your guess letter: " << std::endl;
        std::cin >> GuessedLetter;

        GuessedLetters += GuessedLetter;

        if (ActualWord.find(GuessedLetter) != std::string::npos) {
            for (int i = 0; i < ActualWord.length(); i++) {
                if (ActualWord[i] == GuessedLetter) {
                    GuessWord[i] = GuessedLetter;
                }
            }

            std::cout << "Correct Guess!"  << std::endl;
            std::cout << "Word: " << GuessWord << std::endl;
            std::cout << "Guessed Letters: " << GuessedLetters << std::endl;

        } else {
            IncorrectGuessCount += 1;
            std::cout << "Incorrect Guess!"  << std::endl;
            std::cout << "Word: " << GuessWord << std::endl;
            std::cout << "Guessed Letters: " << GuessedLetters << std::endl;
        }

        if (GuessWord == ActualWord && IncorrectGuessCount < 7) {
            std::cout << "You won! Word was: " << ActualWord << std::endl;
            GameComplete = true;
        }

        if (IncorrectGuessCount > 6) {
            std::cout << "Game Over!" << std::endl;
            GameComplete = true;
        }

        GuessCount++;
    }

    return 0;
}

