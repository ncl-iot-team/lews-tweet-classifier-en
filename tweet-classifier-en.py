from procstream import StreamProcessMicroService
import os
import logging as logger
import spacy

config = {"MODULE_NAME": os.environ.get('MODULE_NAME', 'LEWS_LANG_DETECT'),
          "CONSUMER_GROUP": os.environ.get("CONSUMER_GROUP", "LEWS_LANG_DETECT_CG")}


class StreamProcessClassifyEnglishTweets(StreamProcessMicroService):
    def __init__(self, config_new, en_natural_hazard_model):
        super().__init__(config_new)
        self.en_natural_hazard_model = en_natural_hazard_model

    def process_message(self, message):
        payload = message.value
        if payload.get("lews_meta_detected_lang") == "en" \
                and payload.get("lang") == "en":
            payload["lews-meta-en_class_flag"] = "True"
            payload = self.classify_natural_hazard(payload)
            # logger.debug(payload)
        else:
            # Skip record in case of non-en tweet
            return None
        return payload

    def classify_natural_hazard(self, tweet_record):
        doc = self.en_natural_hazard_model(tweet_record.get('text'))
        tweet_record['lews-meta_is_natural_hazard_related'] = 0
        if doc.cats['POSITIVE'] >= 0.5:
            tweet_record['lews-meta_is_natural_hazard_related'] = 1
        return tweet_record


def main():
    en_natural_hazard_model = spacy.load('english_natural_hazard_model')
    k_service = StreamProcessClassifyEnglishTweets(config, en_natural_hazard_model)
    k_service.start_service()


if __name__ == "__main__":
    main()
