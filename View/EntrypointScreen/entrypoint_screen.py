from View.base_screen import BaseScreenView


class EntrypointScreenView(BaseScreenView):

    def __init__(self, *args, **kwargs) -> None:
        super(EntrypointScreenView, self).__init__(*args, **kwargs)

    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """
