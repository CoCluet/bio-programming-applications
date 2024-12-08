<p align="center">
  <img src="readme_images/park.png" width="400"/>
</p>

# Bio-Inspired Programming applications

The goal of this project is to explore bio-inspired programming methods in a fun and creative way, using them to solve complex problems through simple and illustrative examples.

The paper related to this project is available [here](https://drive.google.com/file/d/151fWkm8I4rPivMh42d5af0V1VV9KUmJV/view?usp=drive_link).

## Problems and methods Overview

This project presents two popular bio-inspired methods:

**1. NEAT (NeuroEvolution of Augmenting Topologies)**

This method is an artificial evolution algorithm designed to optimize both the topology and weights of neural networks. We apply this method to teach a car to drive on a circuit, by making the right decision at the right time.



**2. ACO (Ant Colony Optimization)**

Inspired by the behavior of ant colonies in nature, ACO is a combinatorial optimization algorithm commonly used for problems like graph traversal and routing. This method will be used to park a car in a parking space, by finding the right path.


## Getting Started

### Dependencies

Install the dependencies using the following command:
```
pip install -r requirements.txt
```

### Running the  program

To run the program, use the following command:
```bash
python main.py [option]
```
**Available option:**

| Option            | Description                             |
| :---------------- | :-------------------------------------- |
| `--method`        | Specify the method to run (ACO or NEAT) |

### Customization

You can modify the different parameters to explore and understand different behaviors of the algorithms.

**1) ACO parameters**

Located in the file:
- `ACO/config1.json` for the first problem.
- `ACO/config2.json` for the second problem.
  
**Note**: You can choose the problem in the \_\_init__ method of the classe Engine,  in the file `ACO/engine.py`.

**2) NEAT parameters**

Adjustable in the file `NEAT/config.txt`.

## Authors

- **Corentin CLUET**
  
  Contact: cluetcorentin@gmail.com


## Acknowledgments

* [monokim](https://github.com/monokim/framework_tutorial)
