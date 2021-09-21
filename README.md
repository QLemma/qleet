<p align="left">
  <!-- Continious Integration -->
  <a href="https://github.com/QLemma/qleet/actions?query=workflow%3A%22Continuous+Integration%22"><img alt="GitHub Actions status" src="https://img.shields.io/github/workflow/status/QLemma/qleet/Continuous%20Integration/master?logo=github&style=flat-square"></a>
  <!-- UnitaryFund Support -->
  <a href="http://unitary.fund"><img alt="Unitary Fund" src="https://img.shields.io/badge/Supported%20By-UNITARY%20FUND-brightgreen.svg?style=for-the-badge" width=175></a>
  <!-- PyPI -->
  <!--   <a href="https://pypi.org/project/qleet">
    <img src="https://img.shields.io/pypi/v/qleet.svg?style=flat-square" />
  </a> -->
  <!-- License -->
  <a href="https://www.apache.org/licenses/LICENSE-2.0">
    <img src="https://img.shields.io/github/license/QLemma/qleet" />
  </a>
</p>

# qLEET

qLEET is an open-source library for exploring ***Loss landscape***, ***Expressibility***, ***Entangling capability*** and ***Training trajectories*** of noisy parameterized quantum circuits. 

This project is supported by Unitary Fund. 

## Features

1. Will support [Qiskit’s](https://qiskit.org/) and [Cirq’s](https://quantumai.google/cirq) *quantum circuits* and *noise models*.
2. Provides opportunities to improve existing algorithms like *[VQE](https://www.nature.com/articles/ncomms5213)*, *[QAOA](https://arxiv.org/abs/1411.4028)* by utilizing intuitive insights from the ansatz capability and structure of loss landscape.
3. Facilitate research in designing new hybrid quantum-classical algorithms.
   
   

## Examples

### Properties of an Ansatz

#### Ansatz

<img src="images/ansatz.png" alt="ansatz" width=280 />

#### Expressibility

<img src="images/expressibility.gif" alt="Expressibility" width=480 />

### Solving MAX-CUT using QAOA 

#### Graph

![graph](images/graph.png)

#### Loss Landscape

![losslandscape](images/losslandscape.gif)

#### Training Path

<img src="images/trainingpath.gif" alt="trainingpath" width=480 />
<!-- ![trainingpath](images/trainingpath.gif) -->



## Contributions

We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Submitting a fix
- Proposing new features

Feel free to open an issue on this repository or add a pull request to submit your contribution. Adding test cases for any contributions is a requirement for any pull request to be merged

## References

1. [Expressibility and Entangling Capability of Parameterized Quantum Circuits for Hybrid Quantum‐Classical Algorithms](https://onlinelibrary.wiley.com/doi/abs/10.1002/qute.201900070), Sim, S., Johnson, P. D., & Aspuru‐Guzik, A. Advanced Quantum Technologies, 2(12), 1900070. Wiley. (2019)
2. [Visualizing the Loss Landscape of Neural Nets](https://arxiv.org/abs/1712.09913), Hao Li, Zheng Xu, Gavin Taylor, Christoph Studer, Tom Goldstein, NIPS 2018, arXiv:1712.09913 [cs.LG] (2018)
