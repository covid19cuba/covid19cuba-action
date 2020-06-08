from .municipalities_generator import generate as generate_municipalities
from .national_generator import generate as generate_national
from .provinces_generator import generate as generate_provinces


def generate(debug=False):
    generate_municipalities(debug)
    generate_national(debug)
    generate_provinces(debug)
