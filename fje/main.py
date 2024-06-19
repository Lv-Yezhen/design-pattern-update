import argparse
from .style import StyledJSONBuilder
from .exception import FJEException

def parse_args():
    parser = argparse.ArgumentParser(description='Funny JSON Explorer')
    parser.add_argument('-f', '--file', type=str, help='JSON file path', required=True)
    parser.add_argument('-s', '--style', type=str, help='style', default='tree')
    parser.add_argument('-i', '--icon-family', type=str, help='icon family', default='default')
    parser.add_argument('-c', '--config', type=str, help='icon family file')
    parser.add_argument('-v', '--verbose', action='store_true', help='print availavle icon families and styles', default=False)
    return parser.parse_args()

def main():
    try:
        args = parse_args()
        builder = StyledJSONBuilder()
        if args.config is not None:
            builder.load_icon_family(args.config)
        if args.verbose:
            print(f'available icon families: {builder.get_available_icon_families()}')
            print(f'available styles: {builder.get_available_styles()}')
        builder.create_styled_json(args.file, args.icon_family, args.style).render()
    except FJEException as e:
        print(f'Error: {e}')
    