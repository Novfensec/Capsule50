from Model.base_model import BaseScreenModel


class EntrypointScreenModel(BaseScreenModel):
    """
    Implements the logic of the
    :class:`~View.entrypoint_screen.EntrypointScreen.EntrypointScreenView` class.
    """

    def __init__(self, **kwargs) -> None:
        super(EntrypointScreenModel, self).__init__(**kwargs)
