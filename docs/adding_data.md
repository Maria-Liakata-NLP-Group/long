# Adding Data

Currently, there is no method to add data from within LoNG. Data must be programmatically prior to launching LoNG.

> ** All the solutions on this page are imperfect and are WIP. They will likely be revised later in the project**

The webgui has a dropdown menu in then top left that allows the user to switch between available datasets. If the Talklife data is available, it should show by default. If not the Radom Demo data will be displayed.


### Default Random Demo data

If no other data is available LoNG will load the default random data. This is synthetic data. It is only intended to provide a visual approximation to aggregated social media data. It makes no claims to be statistically meaningful or realistic. Its uses are limited to demonstrating and developing LoNG functionality.

### Talklife data (not publicly available)

Timeline data from Talklife is available only to invited researchers.

The private repo `timeline_selection` can be used to load aggregated Talklife data. The module `data.tl_generation_wrapper` acts as a wrapper for `timeline_selection` repo.

To load Talklife data using the `timeline_selection` repo:

1. Install LoNG, [as described elsewhere](installation.md).
1. Clone  `timeline_selection` locally on your system.
1. If necessary install any additional requirements for `timeline_selection` in your local environment. These include:
    `matplotlib`
1. As required, adjust paths to the pickle files in the `timeline_selection` code.
1. In `src/data/tl_generation_wrapper.py` update the variable `TL_GENERATION_PATH` with either the absolute or relative path to root of the `timeline_selection` clone.

If these steps are completed correctly then the Talklife data should be available to LoNG

long_data = catalogue.get_source("random_data")

"talklife-aggregated"

If these steps are completed correctly then the Talklife data should be available to LoNG
(This solution is imperfect, and will likely be revised later in the project)
