import json, shlex, subprocess


class PlateReader:
    def __init__(self):
        # webcam subprocess args
        webcam_command = "fswebcam -r 640x480 -S 20 --no-banner --quiet ./templates/alpr.jpg"
        self.webcam_command_args = shlex.split(webcam_command)

        #alpr subprocess args
        alpr_command = "alpr -c eu -n 300 -j ./templates/alpr.jpg"
        self.alpr_command_args = shlex.split(alpr_command)


    def webcam_subprocess(self):
        return subprocess.Popen(self.webcam_command_args, stdout=subprocess.PIPE)


    def alpr_subprocess(self):
        return subprocess.Popen(self.alpr_command_args, stdout=subprocess.PIPE)


    def alpr_json_results(self):
        self.webcam_subprocess().communicate()
        alpr_out, alpr_error = self.alpr_subprocess().communicate()

        if not alpr_error is None:
            return None, alpr_error
        elif "No license plates found." in alpr_out:
            return None, None

        try:
            return json.loads(alpr_out), None
        except ValueError, e:
            return None, e


    def read_plate(self):
        alpr_json, alpr_error = self.alpr_json_results()

        if not alpr_error is None:
            return alpr_error

        if alpr_json is None:
            return "No results!"

        results = alpr_json["results"]

        ordinal = 0
        response = []
        for result in results:
            candidates = result["candidates"]

            for candidate in candidates:
                if candidate["matches_template"] == 1:
                    ordinal += 1
                    response[ordinal] = "Guess {0:d}: {1:s} {2:.2f}%".format(ordinal, candidate["plate"],
                                                                             candidate["confidence"])
            return response
