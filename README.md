# Scrabble Game II with bot - Foundations of Programming (FP)

A Python programming project developed for the FP course (2025/2026) at Instituto Superior Técnico (IST), expanding the Scrabble Game I with Abstract Data Types (ADTs) and automated computer agents.

### Evaluation
* Final Grade: 18.7/20.0
	* Automated Assessment: 11.5/12.0
	* Data Abstraction: 4/4
	* Code Quality: 3.3/4.0
 
### Project Features
* Data Abstraction (ADTs): Full encapsulation of internal game components including Board, House, Player, and Vocabulary representations
* Advanced Vocabulary Processing: Features an optimized word parser that reads, filters, and loads custom dictionaries from external text files
* Auto-Solver Pattern Matching: Algorithms to scan the active board for subpatterns and compute the highest-scoring moves 
* Bots: Automated agents capable of playing, passing, or exchanging tiles based on three distinct difficulty levels.

### Run

Load the script using Python:
```bash
python3 FP2526P2.py
```

Launch game with 1 player and 2 bots, vocabulary file, and seed:
```python
scrabble2(('João', '@MEDIO', '@DIFICIL'), 'words.txt', 12345)
```
