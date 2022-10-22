- register keyboard handlers (with precedence?) Basically dictionary of keys, which call sequence of handlers that each can choose if they make some change to the data model

______________________________________________________________________

```puml
class ModelStateInterface
    TBD - would be nice to have a single source of truth (i.e. SQLite tables?) but easy to reason about or use an alternative

class ModelInterface

class PresenterInterface
    model: ModelInterface

---

class Settings
    prefix="DPI_"

class ViewInterface
    model: ModelInterface = default()
    presenter: PresenterInterface = default()

    def create() -> None
        # passes the settings here?

class Game
    def add_view()
        register_keyhandlers() < TBD need way for these to be defined in the Presenter? Maybe mapping is in View, but callbacks are in presenter?

    def run() -> None
```

```sh
# builder pattern?

import package
task = TaskWelcome(class=tbd)
app.register(task)
app.run()
# > ?
```
