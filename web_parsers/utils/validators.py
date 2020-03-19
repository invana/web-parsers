def validate_extractor(extractor):
    validation_errors = []
    if extractor.get("extractor_id") is None:
        validation_errors.append("extraction_id cannot be None in extractor {extractor}".format(extractor=extractor))
    if extractor.get("extractor_type") is None:
        validation_errors.append("extractor_type cannot be None in extractor {extractor}".format(extractor=extractor))

    return validation_errors
