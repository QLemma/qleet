<p align="center">
  <a href="https://qleet.readthedocs.io/">
    <img src="https://raw.githubusercontent.com/QLemma/qleet/master/images/logo-qleet.png" alt="qleet" width=60%/>
  </a>
</p>

<a href="https://qleet.readthedocs.io/en/latest/">qLEET</a> is an open-source library for exploring ***Loss landscape***, ***Expressibility***, ***Entangling capability*** and ***Training trajectories*** of noisy parameterized quantum circuits.

<p align="center">
  <!-- Continious Integration -->
  <a href="https://github.com/QLemma/qleet/actions?query=workflow%3A%22Continuous+Integration%22"><img alt="GitHub Actions status" src="https://img.shields.io/github/workflow/status/QLemma/qleet/Continuous%20Integration/master?logo=github&style=flat-square"></a>
  <!-- Read the Docs status -->
  <a href="https://qleet.readthedocs.io/en/latest/"><img alt="Read the Docs status" src="https://img.shields.io/readthedocs/qleet?style=flat-square"></a>
  <!-- Codecov -->
  <a href="https://app.codecov.io/gh/QLemma/qleet"><img src="https://img.shields.io/codecov/c/github/QLemma/qleet?style=flat-square" alt="Codecov"/></a>
  <!-- Codefactor -->
  <a href="https://www.codefactor.io/repository/github/qlemma/qleet"><img src="https://www.codefactor.io/repository/github/qlemma/qleet/badge?style=flat-square" alt="CodeFactor" />   </a>
  <!-- PyPI -->
  <a href="https://pypi.org/project/qLEET/">
    <img src="https://img.shields.io/pypi/v/qleet.svg?style=flat-square" />
  </a>
  <!-- DOI -->
  <a href="https://doi.org/10.5281/zenodo.5650581">
    <img src="https://img.shields.io/badge/doi-10.5281/zenodo.5650581-blue.svg?style=flat-square"/>
  </a>
  <!-- UnitaryFund Support -->
  <a href="http://unitary.fund"><img alt="Unitary Fund" src="https://img.shields.io/badge/Supported%20By-UNITARY%20FUND-brightgreen.svg?style=for-the-badge" width=175></a>
  <!-- License -->
  <a href="https://www.apache.org/licenses/LICENSE-2.0">
    <img src="https://img.shields.io/github/license/QLemma/qleet?style=flat-square" />
  </a>
</p>


## Key Features

1. Will support [Qiskit’s](https://qiskit.org/), [Cirq’s](https://quantumai.google/cirq) and [pyQuil's](https://github.com/rigetti/pyquil) *quantum circuits* and *noise models*.
2. Provides opportunities to improve existing algorithms like *[VQE](https://www.nature.com/articles/ncomms5213)*, *[QAOA](https://arxiv.org/abs/1411.4028)* by utilizing intuitive insights from the ansatz capability and structure of loss landscape.
3. Facilitate research in designing new hybrid quantum-classical algorithms.


## Installation

qLEET requires Python version 3.7 and above. Installation of qLEET, as well as all its dependencies, can be done using pip:

```console
python -m pip install qleet
```

## Examples

### Properties of an Ansatz

#### Ansatz

<img src="https://raw.githubusercontent.com/QLemma/qleet/master/images/ansatz.png" alt="ansatz" width=30% />

#### Expressibility and Entanglement Spectrum

<p float="left">
<img src="https://raw.githubusercontent.com/QLemma/qleet/master/images/expressibility.gif" alt="Expressibility" width=48% />

<img src="https://raw.githubusercontent.com/QLemma/qleet/master/images/entanglement-spectrum" alt="Entanglement Spectrum" width=48% />
</p>

### Solving MAX-CUT using QAOA 

#### Problem Graph

<img src="https://raw.githubusercontent.com/QLemma/qleet/master/images/graph.png" alt="Graph" width=45% />

#### Loss Landscape and Training Trajectories

<p float="left">
<img src="https://raw.githubusercontent.com/QLemma/qleet/master/images/losslandscape.gif" alt="losslandscape" width=48% />

<img src="https://raw.githubusercontent.com/QLemma/qleet/master/images/trainingpath.gif" alt="trainingpath" width=48% />
</p>

## Contributing to qLEET

We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Submitting a fix
- Proposing new features

Feel free to open an issue on this repository or add a pull request to submit your contribution. Adding test cases for any contributions is a requirement for any pull request to be merged

## Financial Support

This project has been supported by [Unitary Fund](https://unitary.fund/).

## License

qLEET is **free** and **open source**, released under the Apache License, Version 2.0.

## References

1. [Expressibility and Entangling Capability of Parameterized Quantum Circuits for Hybrid Quantum‐Classical Algorithms](https://onlinelibrary.wiley.com/doi/abs/10.1002/qute.201900070), Sim, S., Johnson, P. D., & Aspuru‐Guzik, A. Advanced Quantum Technologies, 2(12), 1900070. Wiley. (2019)
2. [Visualizing the Loss Landscape of Neural Nets](https://arxiv.org/abs/1712.09913), Hao Li, Zheng Xu, Gavin Taylor, Christoph Studer, Tom Goldstein, NIPS 2018, arXiv:1712.09913 [cs.LG] (2018)
