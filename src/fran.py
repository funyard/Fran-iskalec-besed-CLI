import urllib.request
import urllib.parse
import ssl
from bs4 import BeautifulSoup
from termcolor import colored


class FRAN(object):
    def __init__(self, beseda) -> None:
        self.beseda = beseda
        self.content = self.get_website(self.beseda)

    def get_website(self, iskana_beseda) -> BeautifulSoup:
        """
        Ustvari bs4 instance s kontekstom.
        Url je url za fran, pri čemer ne gremo na glavno stran, ampak že v URL vpišemo besedo, katero iščemo.
        """
        context = ssl._create_unverified_context()
        requested_url = urllib.request.urlopen(
            f"https://fran.si/iskanje?View=1&Query={urllib.parse.quote(iskana_beseda)}",
            context=context,
        )

        soup = BeautifulSoup(requested_url, "lxml")
        return soup.find_all("div", attrs={"class": "entry-content"})

    def print_to_terminal(self) -> None:
        """
        Ustvarimo while zanko, ki je pravilna, dokler ne vstavimo besede, ki obstaja. Takrat prekinemo zanko.
        Če beseda ne obstaja, pokličemo še enkrat funkcijo get_website(), ki ustvari nov request z novo besedo, ki ima vhod na Franu.
        Da se program ne zapre takoj, pokličemo input(), da čaka na vnos uporabnika.
        """
        while True:
            try:
                for i in range(3):
                    string = self.content[i].text
                    string1 = colored(string.split()[0], "blue", attrs=["bold"])
                    string2 = " ".join(string.split()[1:])

                    # TODO Več line-breakov pri številkah za boljšo berljivost
                    print(f"{string1} {string2}\n\n")
                break
            except:
                print("Ta beseda ne obstaja!")
                iskana_beseda = input("Vnesi besedo, katero iščeš: ")
                self.content = self.get_website(iskana_beseda)

        input("Pritisni ENTER za izhod")


if __name__ == "__main__":
    beseda = input("Vnesi besedo: ")
    fran = FRAN(beseda)
    fran.print_to_terminal()
