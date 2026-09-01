# Statistical Mechanics of Money: LaTeX Paper Project

A computational validation of statistical mechanics principles applied to economic systems through agent-based simulation.

## 📄 Paper Overview

**Title**: Statistical Mechanics of Money: Applying Boltzmann-Gibbs Distributions and Entropy to Economic Dynamics via Agent-Based Simulation

**Purpose**: Physics of Complex Systems exam submission demonstrating:
- Markov processes in agent-based simulations
- Boltzmann-Gibbs distribution emergence
- Gibbs entropy maximization (Second Law)
- Dynamical systems convergence to equilibrium

## 📁 Project Structure

```
Paper/
├── main.tex                    # Master LaTeX document
├── config/preamble.tex         # Shared packages, custom notation
├── chapters/
│   ├── 00_abstract.tex
│   ├── 01_introduction.tex
│   ├── 02_model.tex
│   ├── 03_results.tex
│   └── 04_conclusion.tex
├── appendices/
│   ├── A_mathematics.tex
│   └── B_code.tex
├── bib/references.bib
├── figures/                    # [To be populated from simulations]
├── Makefile
└── README.md
```

## 🔧 Build Instructions

### Compile the paper:
```bash
cd Paper/
make              # Compile to PDF (recommended)
# or
pdflatex main.tex
```

### Build targets:
```bash
make              # Compile PDF
make clean        # Remove auxiliary files
make distclean    # Remove all generated files
make view         # Open PDF
```

## 📊 Simulation Integration

Export figures from:
- `Simulations.ipynb` → `figures/ch03_*.pdf`
- `StockMarket_Simulation.ipynb` → `figures/ch03_*.pdf`

See figures/README.md for export instructions.

## 🎓 Physics Concepts

The paper emphasizes four key frameworks:
1. **Markov Processes** - Random wealth transactions
2. **Gibbs Entropy** - Information-theoretic disorder
3. **Boltzmann-Gibbs Distribution** - Equilibrium wealth form
4. **Dynamical Systems** - Convergence to attractor

## 📝 Quick Start

1. Figures from simulations → `figures/`
2. Run: `make`
3. Open: `main.pdf`

---
**Status**: Scaffolding complete. Ready for content and figure integration.
