
   # def changeEvent(self, event) -> None:
    #     """
    #     Handles the change event for the window state.

    #     This function is called when the window state changes. It checks if the event type is a window state change event.
    #     If it is, it calls the `window_state_changed` method of the `title_bar` object with the current window state.
    #     Then, it calls the `changeEvent` method of the parent class to handle any other change events.
    #     Finally, it accepts the event.

    #     Parameters:
    #         event (QEvent): The event object representing the change event.

    #     Returns:
    #         None
    #     """
    #     if event.type() == QEvent.Type.WindowStateChange:
    #         self.title_bar.window_state_changed(self.windowState())
    #     super().changeEvent(event)
    #     event.accept()

    # def window_state_changed(self, state) -> None:
    #     """
    #     Handles the window state change event.

    #     This function is called when the window state changes. It checks if the window state is maximized.
    #     If it is, it sets the `normal_button` and `max_button` to visible.
    #     If it is not, it sets the `normal_button` and `max_button` to invisible.

    #     Parameters:
    #         state (Qt.WindowState): The current window state.

    #     Returns:
    #         None
    #     """
    #     self.title_bar.window_state_changed(state)
    #     self.normal_button.setVisible(state == Qt.WindowState.WindowMaximized)
    #     self.max_button.setVisible(state != Qt.WindowState.WindowMaximized)

    # def mousePressEvent(self, event) -> None:
    #     """
    #     Handles the mouse press event.

    #     This function is called when the mouse is pressed. It checks if the left mouse button is pressed.
    #     If it is, it sets the `initial_pos` variable to the current mouse position.
    #     Then, it calls the `mousePressEvent` method of the parent class to handle any other mouse press events.
    #     Finally, it accepts the event.

    #     Parameters:
    #         event (QMouseEvent): The mouse event object.

    #     Returns:
    #         None
    #     """
    #     if event.button() == Qt.MouseButton.LeftButton:
    #         self.initial_pos = event.pos()
    #     super().mousePressEvent(event)
    #     event.accept()

    # def mouseMoveEvent(self, event) -> None:
    #     """
    #     Handles the mouse move event.

    #     This function is called when the mouse is moved. It checks if the `initial_pos` variable is set.
    #     If it is, it calculates the difference between the current mouse position and the initial position.
    #     Then, it calls the `mouseMoveEvent` method of the parent class to handle any other mouse move events.
    #     Finally, it accepts the event.

    #     Parameters:
    #         event (QMouseEvent): The mouse event object.

    #     Returns:
    #         None
    #     """
    #     if self.initial_pos is not None:
    #         delta = event.pos() - self.initial_pos
    #         self.window().move(
    #             self.window().x() + delta.x(),
    #             self.window().y() + delta.y(),
    #         )
    #     super().mouseMoveEvent(event)
    #     event.accept()

    # def mouseReleaseEvent(self, event) -> None:
    #     """
    #     Handles the mouse release event.

    #     This function is called when the mouse is released. It sets the `initial_pos` variable to `None`.
    #     Then, it calls the `mouseReleaseEvent` method of the parent class to handle any other mouse release events.
    #     Finally, it accepts the event.

    #     Parameters:
    #         event (QMouseEvent): The mouse event object.

    #     Returns:
    #         None
    #     """
    #     self.initial_pos = None
    #     super().mouseReleaseEvent(event)
    #     event.accept()
    