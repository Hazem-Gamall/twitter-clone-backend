from rest_framework.parsers import FormParser, MultiPartParser


class DictFormParser(FormParser):
    def parse(self, stream, media_type=None, parser_context=None):
        return super().parse(stream, media_type, parser_context).dict()


class DictMultiPartParser(MultiPartParser):
    def parse(self, stream, media_type=None, parser_context=None):
        parsed_request = super().parse(stream, media_type, parser_context)
        parsed_request.data = parsed_request.data.dict()
        parsed_request.files = parsed_request.files.dict()
        return parsed_request
