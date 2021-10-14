class ColabUtils:

    @staticmethod
    def on_colab():
        """Check if the code is running on Google Colab. Source: https://stackoverflow.com/a/53586419"""
        import sys
        return 'google.colab' in sys.modules
