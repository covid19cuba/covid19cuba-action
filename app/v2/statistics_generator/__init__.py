from .municipalities_generator import generate as generate_municipalities
from .national_generator import generate as generate_national
from .provinces_generator import generate as generate_provinces


def generate(debug=False):
    print("Running municipalities generator v2 ...")
    generate_municipalities(debug)
    print("Municipalities data v2 generated")
    print("Running nacional generator v2 ...")
    generate_national(debug)
    print("Nacional data v2 generated")
    print("Running provinces generator v2 ...")
    generate_provinces(debug)
    print("Provinces data v2 generated")
