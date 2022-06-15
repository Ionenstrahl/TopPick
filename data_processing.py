class DataProcessing:

    @staticmethod
    def sort_commons(commons):
        sorted_commons = sorted(commons, key=lambda x: x.winrate, reverse=True)
        return sorted_commons

    @staticmethod
    def retrieve_top_commons(sorted_commons, amount):
        top_commons = []
        colors = ["W", "U", "B", "R", "G", "", "M"]
        for color in colors:
            top_color_commons = []
            for common in sorted_commons:
                if color == "M":
                    if common.color != "W" or \
                            common.color != "U" or \
                            common.color != "B" or \
                            common.color != "R" or \
                            common.color != "G" or \
                            common.color != "":
                        top_color_commons.append(common)
                        if len(top_color_commons) >= amount:
                            break
                else:
                    if common.color == color:
                        top_color_commons.append(common)
                        if len(top_color_commons) >= amount:
                            break
        return top_commons
