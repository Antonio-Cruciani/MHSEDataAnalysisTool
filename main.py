import json
import sys, getopt
from src.readJson import read_json
from src.ValuesFromCollisionTable import ValuesFromCollisionTable


def main(argv):


    try:
        with open(argv) as json_file:
            parameters = json.load(json_file)
    except IOError:
        print('Error! Can not open '+argv)

    if(parameters['collision_table'] == "True"):
        # chiama values from collision table con i parametri
        # NOTA: se fai che ritorna true puoi eseguire tutto in fila
    if(parameters['statistical_anaysis'] == "True"):
        # chiama readjson

    if(parameters['posteriori_analysis'] == "True"):
        # definisci un metodo che naviga nella cartella di output e fa il ttest + intervalli di confidenza
        # tra direzione in e out 




if __name__ == "__main__":
   main(sys.argv[1:])