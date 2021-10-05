import urllib.request
import urllib.parse
import ssl
from bs4 import BeautifulSoup
from termcolor import colored

# TODO Naredi class


def get_website() -> None:
    """
    Ustvari bs4 instance s kontekstom.
    Url je url za fran, pri čemer ne gremo na glavno stran, ampak že v URL vpišemo besedo, katero iščemo.
    """
    global content
    context = ssl._create_unverified_context()
    beseda = input("Vnesi besedo, katero iščeš: ")
    url = f"https://fran.si/iskanje?View=1&Query={urllib.parse.quote(beseda)}"

    requested_url = urllib.request.urlopen(url, context=context)
    soup = BeautifulSoup(requested_url, "lxml")

    content = soup.find_all(
        "div", attrs={"class": "entry-content"}
    )  # entry-content so tisti deli HTML-a, ki vsebujejo besedo, katero iščemo.


def main() -> None:
    """
    Ustvarimo while zanko, ki je pravilna, dokler ne vstavimo besede, ki obstaja. Takrat prekinemo zanko.
    Če beseda ne obstaja, pokličemo še enkrat funkcijo get_website(), ki ustvari nov request z novo besedo, ki ima vhod na Franu.
    Da se program ne zapre takoj, pokličemo input(), da čaka na vnos uporabnika.
    """
    while True:
        try:
            for i in range(3):
                string = content[i].text
                string1 = colored(string.split()[0], "blue", attrs=["bold"])
                string2 = " ".join(string.split()[1:])

                # TODO Več line-breakov pri številkah za boljšo berljivost
                print(f"{string1} {string2}\n\n")
            break
        except IndexError as e:
            print("Ta beseda ne obstaja!")
            get_website()

    input("Pritisni ENTER za izhod")


if __name__ == "__main__":
    get_website()
    main()
