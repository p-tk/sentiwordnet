import yaml
import sys, argparse
from toArgv import toArgv
from nltk.corpus import sentiwordnet as swn

def start(_argv):
    args = parseArgv(_argv)
    word = args['word']
    meanings = define(word)
    formated = map(show,meanings)
    return yaml.dump(formated,default_flow_style=False)

def define(_word):
    return list(swn.senti_synsets(_word))

def show(_meaning):
    sdisp = lambda n: ('{0:+d}%').format(int(100*n))
    disp = lambda n: ('{0:d}%').format(int(100*n))
    return {
        str(_meaning.synset.name()):
            {
                'fairness': disp(_meaning.obj_score()),
                'meaning': str(_meaning.synset.definition()),
                'feeling': sdisp(_meaning.pos_score() - _meaning.neg_score())
            }
    }

def parseArgv(argv):
    sys.argv = argv

    help = {
        'help': 'Basic demo for sentiment wordnet',
        'word': 'Word to look up all sentiments'
    }

    parser = argparse.ArgumentParser(description=help['help'])
    parser.add_argument('word', help=help['word'])

    return vars(parser.parse_args())

def main(*_args, **_flags):
    return start(toArgv(*_args, **_flags))

if __name__ == "__main__":
    print start(sys.argv)

