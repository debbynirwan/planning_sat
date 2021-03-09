# planning_sat
AI Planning as Satisfiability

## About
This library implements Planning as Satisfiability that can be used to solve STRIPS-like AI Planning Problems using PDDL.
When passed the domain and problem representations in PDDL, the library returns Satisfiability and the model if it is satisfiable and None otherwise.

## Documentation
If you are interested in understanding the details, please read my post
at [TBD](https://google.com)

## Installation
```commandline
pip install planning_sat
```
or, you can clone this repository

## Example

### PDDL for representing planning domain and problem
The Dock-Worker Robots Domain and Problem are provided in the [domain](domain) directory.
There are also Simple Domain and Problem in the same directory.
You can create your PDDL files, or you can download them from the internet.

### Use as a CLI Script
You can execute the script directly by passing it the required arguments which are:
* path to the domain file
* path to the problem file
* length of plan

example:
```commandline
python3 davis_putnam.py -d domain/simple-domain.pddl -p domain/simple-problem.pddl -l 1 -f
```

### Including the library in your project
If you want to include the library in your project, you can install it with pip.
The steps are simple:
* Create an encoder object which will encode the Planning Problem to a boolean (propositional) formula in CNF (Conjunctive Normal Form)
* Create a DPLL object which will run **Davis–Putnam–Logemann–Loveland** algorithm over the encoded problem to determine whether it is *satisfiable* or not

```python
import planning_sat.encoder as encoder
from planning_sat.davis_putnam import DavisPutnam

domain_file = "domain/simple-domain.pddl"
problem_file = "domain/simple-problem.pddl"
encoder = encoder.PlanningProblemEncoder(domain_file, problem_file, length=1)
davis_putnam = DavisPutnam()
satisfiable, model = davis_putnam(encoder.propositional_formulas)
```

## pddlpy
pddlpy included in this repo is the work of Hernán M. Foffani, it is copied from [here.](https://github.com/hfoffani/pddl-lib)


## Issues
Please report issues if you found bugs or raise a Pull Request.
