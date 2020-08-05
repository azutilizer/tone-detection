from voice_util import Tone_Detect


def add_routes_to_resource(_api):
    _api.add_resource(Tone_Detect, '/get_tone', strict_slashes=False)
