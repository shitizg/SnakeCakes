from operator import itemgetter
import pickle


class highscores:
    def __init__(self, filename):
        self.filename = filename
        self.high_scores = self.load()

    def load(self):
        try:
            high_scores = []
            with open(self.filename, "rb") as f:
                unpickler = pickle.Unpickler(f)
                high_scores = unpickler.load()
        except IOError:
            print("File %s Doesn't Exist. Creating High Scores List on %s." % (self.filename, self.filename))
            high_scores = self.dummyscores()
            high_scores = sorted(high_scores, key=itemgetter(1), reverse=True)[:10]
            print(high_scores)
            with open(self.filename, 'wb') as f:
                pickle.dump(high_scores, f)
        return high_scores

    def savenewscore(self, name, newscore):
        self.high_scores.append((name, newscore))
        newtopscores = sorted(self.high_scores, key=itemgetter(1), reverse=True)[:10]
        with open(self.filename, 'wb') as f:
            pickle.dump(newtopscores, f)

    def dummyscores(self):
        """Create A New High Score List of Dummies."""
        scores = [
            ('SUPREME OVERLORD', 200),
            ('Count Duku', 190),
            ('Mike', 180),
            ('John', 150),
            ('Sarah', 140),
            ('Rocky', 100),
            ('Gollum', 90),
            ('Pikachu', 50),
            ('Watermelon', 20),
            ('I Suck', 0),
        ]
        return scores

    def tostring(self):
        mystr = ""
        for i, score in enumerate(self.high_scores):
            mystr += "%d. %s - %d\n\t" % (i+1, score[0], score[1])
        return mystr
