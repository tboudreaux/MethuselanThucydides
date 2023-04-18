from MT.setup import app

import MT.api
import MT.views

if __name__ == '__main__':
    import os
    port = os.environ.get("FLASK_PORT", 5515)
    app.run("0.0.0.0", int(port), debug=True)

