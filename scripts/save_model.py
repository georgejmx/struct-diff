from transformers import MarkupLMProcessor, MarkupLMModel


def main():
    processor = MarkupLMProcessor.from_pretrained("microsoft/markuplm-base")
    model = MarkupLMModel.from_pretrained("microsoft/markuplm-base")

    processor.save_pretrained("./models/saved_markup_processor")
    model.save_pretrained("./models/saved_markup_model")


if __name__ == "__main__":
    main()
