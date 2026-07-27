class GestureLibrary:


    def swipe_up(self, driver):

        size = driver.get_window_size()

        start_x = size["width"] / 2
        start_y = size["height"] * 0.8

        end_y = size["height"] * 0.2


        driver.swipe(

            start_x,
            start_y,
            start_x,
            end_y,
            800

        )
