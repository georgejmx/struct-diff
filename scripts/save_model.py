from sentence_transformers import SentenceTransformer


def main():
    model = SentenceTransformer("all-mpnet-base-v2")
    model.save("./models/all-mpnet-base-v2")


if __name__ == "__main__":
    main()
