
from word2cin.post_processing.add_no_tone import AddNoTone
from word2cin.post_processing.convert_key_to_lower_case import ConvertKeyToLowerCase


POST_PROCESSING_OPTIONS = {
    "convert_key_to_lower_case": ConvertKeyToLowerCase,
    "add_no_tone": AddNoTone,
}
