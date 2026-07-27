from libraries.DriverFactory import DriverFactory


class PerfectoLibrary:


    def __init__(self):

        self.driver_factory = DriverFactory()

        self.driver = None



    def open_application(self, platform):

        self.driver = (
            self.driver_factory
            .create_driver(platform)
        )


    def close_application(self):

        self.driver_factory.quit_driver()


    def get_driver(self):

        return self.driver
