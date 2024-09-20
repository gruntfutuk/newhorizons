from gooey import Gooey, GooeyParser

@Gooey
def main():
    parser = GooeyParser(description="My Program")
    parser.add_argument("name", help="Enter your name")
    args = parser.parse_args()
    print(f"Hello, {args.name}!")

if __name__ == "__main__":
    main()
