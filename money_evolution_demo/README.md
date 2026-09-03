# Money Evolution Demonstration

This folder contains two versions of the money-exchange demonstration:

- `Demonstration-Statistical-Mechanics-of-Money-1-0-0-definition.nb` is the original Wolfram Mathematica Demonstration.
- `money_evolution_demo.ipynb` is a Python/Jupyter reimplementation with a time slider and an automatic animation.

The `.ipynb` is not a mechanical file-format conversion. Mathematica's `Manipulate` and Wolfram language expressions cannot run in a normal Python kernel, so the model and visualization have been recreated with NumPy, Matplotlib, and ipywidgets.

## Python/Jupyter version

From the project root, install the dependencies:

```text
python -m pip install -r requirements.txt
```

Start Jupyter and open the notebook:

```text
jupyter lab
```

Run the cells from top to bottom. The notebook will:

1. Define the random-exchange model and entropy calculation.
2. Generate 50 snapshots from 20 economies, each containing 25 agents.
3. Display the money histogram beside the entropy history.
4. Provide an interactive time slider when ipywidgets is available.
5. Create an inline animation and save it as `outputs/money_evolution.gif`.

The simulation begins with every agent holding 100 units. At each exchange, two random agents are selected and a random amount up to 100 units is transferred when the selected donor can afford it. Total money is conserved. Because the model is stochastic, each execution produces a different trajectory, but the distribution should broaden and the entropy should generally rise toward equilibrium.

The GIF is generated with Pillow, so ffmpeg is not required. The `outputs/` directory is intentionally separate from the notebook because the animation is a generated artifact.

## Mathematica version

Open the `.nb` file in Mathematica 14.1 or a compatible Wolfram environment. Evaluate the notebook's initialization and output cells if needed. Its `Manipulate` control is a time slider from 1 to 50: move the slider to inspect the money distribution and entropy at each recorded snapshot. The original file does not contain an automatic `Animate` or `ListAnimate` animation.

## Folder contents

```text
money_evolution_demo/
├── Demonstration-Statistical-Mechanics-of-Money-1-0-0-definition.nb
├── money_evolution_demo.ipynb
├── README.md
└── outputs/
    └── money_evolution.gif   # generated after running the notebook
```
