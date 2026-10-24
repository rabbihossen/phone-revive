# Contributing to PhoneFix

Thank you for your interest in contributing to PhoneFix! We welcome community contributions, brand profiles, bug reports, and optimizations.

## Getting Started

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/your-username/phone-fix.git
   cd phone-fix
   ```

2. Install dev dependencies:
   ```bash
   python3 -m pip install -r requirements-dev.txt
   ```

3. Run the test suite:
   ```bash
   pytest -v
   ```

## Adding a New Brand Profile

To add support for a new Android brand or custom ROM:
1. Create a new profile class in `phone_fix/brands/` subclassing `BaseBrandProfile`.
2. Define the list of `BloatwareItem`s with accurate descriptions and risk levels.
3. Register the brand in `phone_fix/brands/__init__.py`.
4. Add unit tests in `tests/test_brand_adapters.py`.
5. Submit a pull request!

## Safety Guidelines

- Every optimization must be safe, non-destructive, and reversible.
- Never use destructive commands (`pm clear` on core packages, wiping user partitions).
- User 0 package uninstalls must be reversible via `cmd package install-existing`.
