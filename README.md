# Symbolic Cube Explorer

Symbolic Cube Explorer is a small experimental framework for studying symbolic
systems as trajectories through a geometric state space.

Instead of treating symbols as static tokens, this project treats them as
operations acting on the vertices of a cube graph.

A sequence of operations therefore becomes a path through the cube.

Concept → seed vertex → cube trajectory → symbolic sequence → structure score

The project was inspired by historical combinatorial traditions such as
Sefer Yetzirah, which describes letters acting as generative operations,
and by modern ideas in symbolic dynamics and graph-based computation.

## Features

- hypercube state space
- symbolic grammar layer
- trajectory scoring
- 3-D visualization using Plotly

## Installation


git clone https://github.com/Lydia-No/symbolic-cube-explorer.git

cd symbolic-cube-explorer

python3 -m venv .venv
source .venv/bin/activate

pip install -e .


## Example

Run the concept atlas experiment:


python examples/concept_atlas.py


This maps concepts to cube trajectories and generates symbolic sequences.

## Project Structure

src/cube_explorer/core.py  
cube dynamics

src/cube_explorer/grammar.py  
symbolic mapping layer

src/cube_explorer/utils.py  
helpers and hashing

src/cube_explorer/visualization.py  
trajectory visualization

examples/concept_atlas.py  
example experiment

Save with Ctrl+O, then Enter, then Ctrl+X.

Then commit it:

git add README.md
git commit -m "add project documentation"
git push
