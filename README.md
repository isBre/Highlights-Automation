# Highlights-Automation
This script makes it possible to automate the process of creating highlights by giving as input the movies, the corresponding minutes of highlights and banner ads. It will make sure to cut these actions and merge them into a single movie by scrolling up the advertising partners.

## Input
* In a folder named `Minuti` place all the **text files with the minutes** inside that have the salient actions. it is important to make sure that these files are sorted alphabetically so that they correspond to the correct movie. The program will search for files of type `.txt`, any type of other file will be ignored.
* In the `Filmati` folder place the **movies files** that will be divided into clips by the minutes chosen previously. it is important to make sure that these files are sorted alphabetically so that they correspond to the correct text files for the minutes. The program will search for files of type `.mp4`, any type of other file will be ignored.
* In the `Banner` folder place the **banner ads**, the recommended dimension is 300(width)x100(height). Also, if you want to prioritize some ads over others, you can sort them alphabetically. 

![alt text](https://github.com/isBre/Highlights-Automation/blob/main/Images/Screenshot%201.png)

## Output
* A number of `clips` equal to the number of minutes entered in all text files in Minutes.
* The file called `Highlights.mp4` that will contain the concatenated clips with banner ads arranged at the top that will rotate every 3 seconds.

## Use case
I personally use this script to automate the highlights process in a basketball game. During the game I take note of the minutes of the most important baskets all while recording the match. When the game ends I give everything as input to the program and get the final movie.

![alt text](https://github.com/isBre/Highlights-Automation/blob/main/Images/Risorsa%201.png)

## Notes
There are two other scripts in the repository called `OnlyClips.py` and `OnlyConcatenation.py` that allow one to cut the movie into clips and the other to merge clips in a folder and add banner ads. This is useful if you first want to check that the extracted clips are correct.
